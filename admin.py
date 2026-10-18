from django.contrib import admin
from .models import DocumentType, DocumentRequest

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'estimated_days')
    search_fields = ('name',)

@admin.register(DocumentRequest)
class DocumentRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'citizen', 'document_type', 'status', 'created_at')
    list_filter = ('status', 'document_type')
    search_fields = ('citizen__username', 'description')