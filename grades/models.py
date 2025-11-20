from django.db import models


class GradeItem(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='grade_items')
    name = models.CharField(max_length=255)
    weight = models.FloatField(default=1.0)


class Grade(models.Model):
    item = models.ForeignKey(GradeItem, on_delete=models.CASCADE, related_name='grades')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
