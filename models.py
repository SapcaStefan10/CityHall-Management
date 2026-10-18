from django.db import models
from django.contrib.auth.models import User
from .storage import EncryptedFileSystemStorage

class DocumentType(models.Model):
    # building permits, fiscal certificates, etc.
    name = models.CharField(max_length=100, unique=True)
    estimated_days = models.IntegerField(default=30) # in cat timp ar trebui sa fie gata

    def __str__(self):
        return self.name


class CitizenDocument(models.Model):
    # documentele urcate de cetateni in locker (buletin, adeverinte, etc)
    citizen = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=150)
    file = models.FileField(upload_to='citizen_locker/', storage=EncryptedFileSystemStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.citizen.username})"


class DocumentRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    citizen = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)
    description = models.TextField()
    attached_document = models.ForeignKey(
        CitizenDocument, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='requests'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    staff_comments = models.TextField(blank=True, null=True) # explicatii de la primarie (de ce a fost respins, etc)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request #{self.id} - {self.document_type.name}"

