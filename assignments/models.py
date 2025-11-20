from django.db import models
from django.conf import settings
from courses.models import Course


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/', null=True, blank=True)
    data = models.JSONField(default=dict, blank=True)


class AssignmentGrade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grade')
    grader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    score = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
