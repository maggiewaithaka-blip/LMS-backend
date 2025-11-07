from rest_framework import serializers
from .models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'owner', 'file', 'filename', 'content_type', 'size', 'created_at', 'course', 'metadata']
        read_only_fields = ['id', 'created_at']
