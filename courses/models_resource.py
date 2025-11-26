
from django.db import models
from assignments.models import Attachment


class Assignment(models.Model):
	course_section = models.ForeignKey('courses.CourseSection', on_delete=models.CASCADE, related_name='assignments')
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
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


