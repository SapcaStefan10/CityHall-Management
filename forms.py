from django import forms
from .models import DocumentRequest, CitizenDocument

class CitizenDocumentForm(forms.ModelForm):
    class Meta:
        model = CitizenDocument
        fields = ['name', 'file']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'E.g., Identity Card copy'
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class DocumentRequestForm(forms.ModelForm):
    class Meta:
        model = DocumentRequest
        fields = ['document_type', 'description', 'attached_document']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Provide specific details regarding your request...'
            }),
            'attached_document': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['attached_document'].queryset = CitizenDocument.objects.filter(citizen=user)
            self.fields['attached_document'].empty_label = "Select an uploaded document (Optional)"
        else:
            self.fields['attached_document'].queryset = CitizenDocument.objects.none()