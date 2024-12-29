from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import base64
from django.conf import settings
from django_otp.plugins.otp_totp.models import TOTPDevice

# Gera uma chave de criptografia (em um projeto real, armazene isso de forma segura)
# key = Fernet.generate_key()
# cipher_suite = Fernet(key)

# Use a chave de criptografia do arquivo de configurações
cipher_suite = Fernet(settings.ENCRYPTION_KEY)

class Password(models.Model):
    CATEGORY_CHOICES = [
        ('work', 'Work'),
        ('personal', 'Personal'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passwords')
    service_name = models.CharField(max_length=255)
    login = models.CharField(max_length=255)
    password_value = models.CharField(max_length=255)  # Certifique-se de que este campo está definido
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        encrypted_password = cipher_suite.encrypt(raw_password.encode())
        self.password_value = base64.urlsafe_b64encode(encrypted_password).decode()

    def get_password(self):
        return self.password_value

    def __str__(self):
        return self.service_name

class CustomTOTPDevice(TOTPDevice):
    class Meta:
        proxy = True

    def get_step(self):
        return 60