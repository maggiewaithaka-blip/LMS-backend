from django.db import models

class StudentApplication(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    nationality = models.CharField(max_length=100)
    qualification = models.CharField(max_length=255)
    knqf_level = models.CharField(max_length=50)
    academic_certificate = models.FileField(upload_to='applications/certificates/')
    passport_photo = models.ImageField(upload_to='applications/photos/')
    national_id = models.FileField(upload_to='applications/ids/', null=True, blank=True)
    passport = models.FileField(upload_to='applications/passports/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"{self.full_name} ({self.email})"
