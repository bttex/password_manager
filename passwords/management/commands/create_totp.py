from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode
import os

class Command(BaseCommand):
    help = 'Cria um dispositivo TOTP para um usuário específico'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username do usuário')

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=options['username'])
            # Remove dispositivos existentes
            TOTPDevice.objects.filter(user=user).delete()
            # Cria novo dispositivo
            device = TOTPDevice.objects.create(
                user=user, 
                name='default',
                step=60,
                t0=0,
                digits=6,
                tolerance=1
            )
            device.confirmed = True
            device.save()
            
            # Gera QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(device.config_url)
            qr.make(fit=True)
            
            # Salva QR code como imagem
            img = qr.make_image(fill_color="black", back_color="white")
            qr_path = os.path.join(os.getcwd(), 'totp_qr.png')
            img.save(qr_path)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'TOTP criado com sucesso para {user.username}\n'
                    f'Secret Key: {device.bin_key}\n'
                    f'URL de Configuração: {device.config_url}\n'
                    f'QR Code salvo em: {qr_path}'
                )
            )
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Usuário {options["username"]} não encontrado'))