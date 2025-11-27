from django.db import models
from django.conf import settings
# Removed: from assignments.models import Attachment  <-- This was the crash source


class CourseCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name


class Course(models.Model):
    shortname = models.CharField(max_length=100, unique=True)
    fullname = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    visible = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    # The 'users.User' string reference is correct and safe
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_courses')

    def __str__(self):
        return self.fullname


class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=0)
    # assignments, quizzes, resources are now related via ForeignKey in their respective models
    notifications = models.TextField(blank=True, help_text="Messages or notifications for this section")
    storage = models.TextField(blank=True, help_text="Uploaded documents or file references")


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.course.fullname})"