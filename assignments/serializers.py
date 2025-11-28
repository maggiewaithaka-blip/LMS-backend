from rest_framework import serializers
from .models import AssignmentGrade, Attachment



class AttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = ['id', 'type', 'file_url', 'url', 'text', 'created_at']

    def get_file_url(self, obj):
        if obj.file:
            try:
                return obj.file.url
            except Exception:
                return None
        return None


class AssignmentGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentGrade
        fields = ['id', 'grader', 'score', 'feedback']  # Removed 'submission'
