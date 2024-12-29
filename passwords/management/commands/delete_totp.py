from django.core.management.base import BaseCommand
from django_otp.plugins.otp_totp.models import TOTPDevice

class Command(BaseCommand):
    help = 'Deleta todos os dispositivos TOTP'

    def handle(self, *args, **options):
        count = TOTPDevice.objects.all().delete()[0]
        self.stdout.write(
            self.style.SUCCESS(f'Deletados {count} dispositivos TOTP')
        )