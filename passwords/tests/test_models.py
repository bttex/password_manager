from django.test import TestCase
from django.contrib.auth.models import User
from passwords.models import Password

class PasswordModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_password_creation(self):
        password = Password.objects.create(
            user=self.user,
            site='Test Site',
            username='testuser',
            encrypted_password='encrypted_password'
        )
        self.assertEqual(password.site, 'Test Site')
        self.assertEqual(password.username, 'testuser')