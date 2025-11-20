from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Role, UserRole

class Command(BaseCommand):
    help = 'Assigns the student role to all users who do not have any role.'

    def handle(self, *args, **options):
        User = get_user_model()
        role_obj, _ = Role.objects.get_or_create(name='student')
        count = 0
        for user in User.objects.all():
            if not UserRole.objects.filter(user=user).exists():
                UserRole.objects.create(user=user, role=role_obj)
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Assigned student role to {count} users.'))
