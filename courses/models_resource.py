from django.db import models

class Assignment(models.Model):
    section = models.ForeignKey('courses.CourseSection', on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    section = models.ForeignKey('courses.CourseSection', on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Resource(models.Model):
    section = models.ForeignKey('courses.CourseSection', on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title