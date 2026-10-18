from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from core.views import (
    landing_page_view, login_view, logout_view, dashboard_view, create_request_view,
    staff_dashboard_view, update_status_view, register_view,
    documents_dashboard_view, upload_document_view, delete_document_view,
    secure_download_view, view_certificate
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/new-request/', create_request_view, name='create_request'),
    path('staff/', staff_dashboard_view, name='staff_dashboard'),
    path('staff/update/<int:request_id>/<str:status>/', update_status_view, name='update_status'),
    path('documents/', documents_dashboard_view, name='documents_dashboard'),
    path('documents/upload/', upload_document_view, name='upload_document'),
    path('documents/delete/<int:doc_id>/', delete_document_view, name='delete_document'),
    path('documents/download/<int:doc_id>/', secure_download_view, name='secure_download'),
    path('documents/issued/<int:request_id>/certificate/', view_certificate, name='view_certificate'),
    
    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='core/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)