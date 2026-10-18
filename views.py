from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
import mimetypes
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from .models import DocumentRequest, CitizenDocument, DocumentType
from .forms import DocumentRequestForm, CitizenDocumentForm

def is_staff_user(user):
    return user.is_staff

def landing_page_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff_dashboard')
        return redirect('dashboard')
    return render(request, 'core/landing.html')

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff_dashboard')
        return redirect('dashboard')

    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        user = authenticate(request, username=username_input, password=password_input)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('staff_dashboard')
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! Welcome to your Dashboard.")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard_view(request):
    if request.user.is_staff:
        return redirect('staff_dashboard')
    user_requests = DocumentRequest.objects.filter(citizen=request.user).order_by('-created_at')
    return render(request, 'core/dashboard.html', {'requests': user_requests})

@login_required
def create_request_view(request):
    if request.user.is_staff:
        return redirect('staff_dashboard')

    if request.method == 'POST':
        form = DocumentRequestForm(request.POST, user=request.user)
        if form.is_valid():
            document_request = form.save(commit=False)
            document_request.citizen = request.user
            document_request.save()
            messages.success(request, "Your document request has been submitted successfully.")
            return redirect('dashboard')
    else:
        form = DocumentRequestForm(user=request.user)
    
    has_docs = CitizenDocument.objects.filter(citizen=request.user).exists()
    return render(request, 'core/create_request.html', {'form': form, 'has_docs': has_docs})

@login_required
@user_passes_test(is_staff_user, login_url='dashboard')
def staff_dashboard_view(request):
    all_requests = DocumentRequest.objects.all().order_by('-created_at')
    return render(request, 'core/staff_dashboard.html', {'requests': all_requests})

@login_required
@user_passes_test(is_staff_user, login_url='dashboard')
def update_status_view(request, request_id, status):
    doc_request = get_object_or_404(DocumentRequest, id=request_id)
    if request.method == 'POST':
        comments = request.POST.get('staff_comments', '')
        doc_request.status = status.upper()
        doc_request.staff_comments = comments
        doc_request.save()
        messages.success(request, f"Request #{request_id} updated to {status.upper()}.")
    else:
        doc_request.status = status.upper()
        doc_request.save()
        messages.success(request, f"Request #{request_id} marked as {status.upper()}.")
    return redirect('staff_dashboard')

@login_required
def documents_dashboard_view(request):
    if request.user.is_staff:
        return redirect('staff_dashboard')
        
    uploaded_docs = CitizenDocument.objects.filter(citizen=request.user).order_by('-uploaded_at')
    issued_requests = DocumentRequest.objects.filter(citizen=request.user, status='APPROVED').order_by('-created_at')
    
    form = CitizenDocumentForm()
    return render(request, 'core/documents_dashboard.html', {
        'uploaded_docs': uploaded_docs,
        'issued_requests': issued_requests,
        'form': form
    })

@login_required
def upload_document_view(request):
    if request.user.is_staff:
        return redirect('staff_dashboard')
        
    if request.method == 'POST':
        form = CitizenDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.citizen = request.user
            doc.save()
            messages.success(request, f"Document '{doc.name}' uploaded successfully to your locker.")
        else:
            messages.error(request, "Failed to upload document. Please check the file format.")
    return redirect('documents_dashboard')

@login_required
def delete_document_view(request, doc_id):
    if request.user.is_staff:
        return redirect('staff_dashboard')
        
    doc = get_object_or_404(CitizenDocument, id=doc_id, citizen=request.user)
    doc.file.delete()
    doc.delete()
    messages.success(request, "Document removed from locker.")
    return redirect('documents_dashboard')

@login_required
def secure_download_view(request, doc_id):
    doc = get_object_or_404(CitizenDocument, id=doc_id)
    if doc.citizen != request.user and not request.user.is_staff:
        raise Http404("Document not found or unauthorized.")
        
    try:
        file = doc.file.open('rb')
        content = file.read()
    except Exception:
        raise Http404("File not found on server.")
        
    content_type, encoding = mimetypes.guess_type(doc.file.name)
    response = HttpResponse(content, content_type=content_type or 'application/octet-stream')
    return response

@login_required
def view_certificate(request, request_id):
    doc_request = get_object_or_404(DocumentRequest, id=request_id)
    if not request.user.is_staff and doc_request.citizen != request.user:
        messages.error(request, "Unauthorized access.")
        return redirect('dashboard')
        
    if doc_request.status != 'APPROVED':
        messages.error(request, "Certificate is not available yet.")
        return redirect('dashboard')
        
    return render(request, 'core/certificate.html', {'request': doc_request})
