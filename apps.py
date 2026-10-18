from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from core.models import DocumentType
        document_types = [
            'Fiscal Certificate',
            'Building Permit',
            'Certificate of Urbanism',
            'ID Renewal Request'
        ]
        try:
            for name in document_types:
                DocumentType.objects.get_or_create(name=name)
        except:
            pass