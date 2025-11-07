from django.db import models
from django.conf import settings


class Quiz(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_limit = models.IntegerField(null=True, blank=True, help_text='Time limit in seconds')
    attempts_allowed = models.IntegerField(default=1)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=50)
    text = models.TextField()
    data = models.JSONField(default=dict, blank=True)


class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    data = models.JSONField(default=dict, blank=True)


class QuestionResponse(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.JSONField(default=dict, blank=True)
    correct = models.BooleanField(null=True, blank=True)
