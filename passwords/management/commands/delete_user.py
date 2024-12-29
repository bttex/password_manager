from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Deleta usuários do sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username específico para deletar',
            required=False
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Deleta todos os usuários exceto superuser',
            required=False
        )

    def handle(self, *args, **options):
        if options['all']:
            users = User.objects.filter(is_superuser=False)
            count = users.count()
            users.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Deletados {count} usuários')
            )
        elif options['username']:
            try:
                user = User.objects.get(username=options['username'])
                user.delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Usuário {options["username"]} deletado com sucesso')
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Usuário {options["username"]} não encontrado')
                )
        else:
            self.stdout.write(
                self.style.ERROR('Especifique --username ou --all')
            )