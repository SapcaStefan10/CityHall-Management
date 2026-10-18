from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import DocumentType, CitizenDocument, DocumentRequest

class CityHallPortalTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.doc_type = DocumentType.objects.create(name="Building Permit", estimated_days=10)
        
        # un user normal (cetatean)
        self.citizen = User.objects.create_user(username="citizen1", password="password123")
        
        # un user de staff
        self.staff = User.objects.create_superuser(username="staff1", password="password123", email="staff@cityhall.gov")
        self.staff.is_staff = True
        self.staff.save()

    def test_pages_require_login(self):
        # daca nu esti logat, te redirectioneaza
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('login' in response.url)

        response = self.client.get(reverse('documents_dashboard'))
        self.assertEqual(response.status_code, 302)
        
    def test_login_page_renders(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')

    def test_authenticated_citizen_dashboard(self):
        self.client.login(username="citizen1", password="password123")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/dashboard.html')

    def test_document_locker_views(self):
        self.client.login(username="citizen1", password="password123")
        response = self.client.get(reverse('documents_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/documents_dashboard.html')

    def test_staff_dashboard_permissions(self):
        # cetateanul nu ar trebui sa aiba acces la panoul de staff
        self.client.login(username="citizen1", password="password123")
        response = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(response.status_code, 302)
        
        # staff-ul da, ar trebui sa mearga
        self.client.login(username="staff1", password="password123")
        response = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/staff_dashboard.html')


