from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.conf import settings
from cryptography.fernet import Fernet

class EncryptedFileSystemStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fernet = Fernet(settings.ENCRYPTED_FILE_KEY)

    def _save(self, name, content):
        content_bytes = content.read()
        encrypted_data = self.fernet.encrypt(content_bytes)
        return super()._save(name, ContentFile(encrypted_data))

    def _open(self, name, mode='rb'):
        file = super()._open(name, 'rb')
        encrypted_data = file.read()
        
        try:
            decrypted_data = self.fernet.decrypt(encrypted_data)
        except Exception:
            file.seek(0)
            decrypted_data = encrypted_data
            
        if 't' in mode or mode == 'r':
             return ContentFile(decrypted_data.decode('utf-8'))
        return ContentFile(decrypted_data)
