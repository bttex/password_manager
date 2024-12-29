from django.test import TestCase
from django.contrib.auth.models import User
from passwords.forms import PasswordForm

class FormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_password_form_valid(self):
        form_data = {
            'site': 'Test Site',
            'username': 'testuser',
            'encrypted_password': 'testpass123'
        }
        form = PasswordForm(data=form_data)
        if not form.is_valid():
            print(form.errors)  # Debug
        self.assertTrue(form.is_valid())