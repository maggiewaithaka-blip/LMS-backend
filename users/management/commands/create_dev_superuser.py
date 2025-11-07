from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a development superuser if it does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'devadmin'
        email = 'devadmin@example.local'
        password = 'DevPassw0rd!'
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Created superuser {username}'))
        else:
            self.stdout.write('Superuser already exists')
