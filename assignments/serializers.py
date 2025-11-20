from rest_framework import serializers
from .models import Assignment, Submission, AssignmentGrade


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'course', 'title', 'description', 'due_date']


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'user', 'submitted_at', 'file', 'data']
        read_only_fields = ['id', 'submitted_at']


class AssignmentGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentGrade
        fields = ['id', 'submission', 'grader', 'score', 'feedback']
