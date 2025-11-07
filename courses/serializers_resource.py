from rest_framework import serializers
from .models_resource import CourseResource
from storage.serializers import FileSerializer
from storage.models import File as StorageFile


class CourseResourceSerializer(serializers.ModelSerializer):
    file = serializers.PrimaryKeyRelatedField(queryset=StorageFile.objects.all(), allow_null=True, required=False)
    download_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CourseResource
        fields = ['id', 'course', 'title', 'resource_type', 'file', 'url', 'content', 'created_at', 'download_url']
        read_only_fields = ['id', 'created_at', 'download_url']

    def get_download_url(self, obj):
        try:
            return obj.get_download_url()
        except Exception:
            return None
