from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from .models_scorm import *
class CourseCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name


class Course(models.Model):
    shortname = models.CharField(max_length=100, unique=True)
    fullname = models.CharField(max_length=255)
    summary = RichTextField(blank=True)
    thumbnail = models.ImageField(blank=True, null=True, upload_to='course_thumbnails/')
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
    summary = RichTextField(blank=True)
    position = models.PositiveIntegerField(default=0)
    notifications = RichTextField(blank=True, help_text="Messages or notifications for this section")
    storage = RichTextField(blank=True, help_text="Uploaded documents or file references")
    visible = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} ({self.course.fullname})"


class Assignment(models.Model):
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True)
    text = RichTextField(blank=True)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True)
    text = RichTextField(blank=True)

    def __str__(self):
        return self.title


class Resource(models.Model):
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True)
    text = RichTextField(blank=True)

    def __str__(self):
        return self.title


class Attachment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    type = models.CharField(max_length=50, choices=[
        ('file', 'File'),
        ('url', 'URL'),
        ('text', 'Text'),
        ('pdf', 'PDF'),
        ('audio', 'Audio'),
        ('video', 'Video'),
    ], default='file')
    file = models.FileField(upload_to='attachments/', null=True, blank=True)
    url = models.URLField(blank=True)
    text = RichTextField(blank=True)
##for deployment purpose
    def __str__(self):
        return f"Attachment ({self.type})"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = RichTextField(blank=True)
    position = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.course.fullname})"