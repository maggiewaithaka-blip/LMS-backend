
from django.db import models
# REMOVED: from assignments.models import Attachment 
# FIX: The model definition below will now use a string literal to reference Attachment.

# Removed this import. The models below (Assignment, Quiz, Resource) must be 
# in the file *where they are intended to be defined*.

class Assignment(models.Model):
    course_section = models.ForeignKey('courses.CourseSection', on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # FIX: If you intended to have a link here, you must use a string literal.
    # If the intention was for the Attachment model to link *back* to Assignment, 
    # then this is unnecessary and the Attachment model's ForeignKey is enough.
    # Assuming Attachment links back to Assignment, no field is needed here.

    def __str__(self):
        return self.title


class Quiz(models.Model):
    course_section = models.ForeignKey('courses.CourseSection', on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Resource(models.Model):
    course_section = models.ForeignKey('courses.CourseSection', on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title