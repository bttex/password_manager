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
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='stored_passwords'
    )
    site = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    encrypted_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        encrypted_password = cipher_suite.encrypt(raw_password.encode())
        self.encrypted_password = base64.urlsafe_b64encode(encrypted_password).decode()

    def get_password(self):
        return self.encrypted_password

    def __str__(self):
        return f"{self.site} - {self.username}"

class CustomTOTPDevice(TOTPDevice):
    class Meta:
        proxy = True

    def get_step(self):
        return 60

    def verify_token(self, token):
        # Certifique-se de que o passo está sendo aplicado corretamente
        self.step = 60
        return super().verify_token(token)