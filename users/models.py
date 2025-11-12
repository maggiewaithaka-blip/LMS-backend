from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Extend with fields commonly used in Moodle mapping
    timezone = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    institution = models.CharField(max_length=255, blank=True, null=True)

    def has_role(self, role_name: str) -> bool:
        """Return True if the user has a Role with the given name."""
        return UserRole.objects.filter(user=self, role__name=role_name).exists()

    def has_any_role(self, role_names) -> bool:
        """Return True if the user has any role in the iterable role_names."""
        return UserRole.objects.filter(user=self, role__name__in=role_names).exists()


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    shortname = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='profile')
    passport_photo = models.ImageField(upload_to='profiles/passport_photos/', blank=True, null=True)
    national_id = models.FileField(upload_to='profiles/national_ids/', blank=True, null=True)
    passport = models.FileField(upload_to='profiles/passports/', blank=True, null=True)
    academic_certificate = models.FileField(upload_to='profiles/certificates/', blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    qualification_level = models.CharField(max_length=64, blank=True, null=True)
    field_of_study = models.CharField(max_length=128, blank=True, null=True)
    nationality = models.CharField(max_length=64, blank=True, null=True)
