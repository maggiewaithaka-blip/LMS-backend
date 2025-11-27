from django.db import models
from django.conf import settings
# REMOVED: from courses.models import Course # This import caused the circular dependency


class EnrollmentMethod(models.Model):
    name = models.CharField(max_length=100)
    config = models.JSONField(default=dict, blank=True)


class Enrollment(models.Model):
    # This remains correct
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')

    # FIX: Using the string literal 'courses.Course' prevents the immediate module import crash.
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE) 
    
    method = models.ForeignKey(EnrollmentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50, default='student')