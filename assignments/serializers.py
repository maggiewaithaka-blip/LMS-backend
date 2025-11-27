from rest_framework import serializers
from .models import Assignment, Submission, AssignmentGrade


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'course', 'title', 'description', 'due_date']



class SubmissionSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'user', 'submitted_at', 'file', 'data']
        read_only_fields = ['id', 'submitted_at']

    def get_file(self, obj):
        if obj.file:
            try:
                return obj.file.url
            except Exception:
                return None
        return None


class AssignmentGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentGrade
        fields = ['id', 'submission', 'grader', 'score', 'feedback']
