from rest_framework import serializers
from .models_scorm import ScormPackage
from django.conf import settings


class ScormPackageSerializer(serializers.ModelSerializer):
    launch_url = serializers.SerializerMethodField()

    class Meta:
        model = ScormPackage
        fields = ['id', 'name', 'zip_file', 'uploaded_at', 'launch_url']

    def get_launch_url(self, obj):
        # Use the extracted_path property (not a DB field)
        extracted_path = getattr(obj, 'extracted_path', None)
        if extracted_path:
            rel_path = extracted_path.replace(str(settings.MEDIA_ROOT), '').lstrip('/\\')
            rel_path = rel_path.replace('\\', '/')  # Ensure forward slashes for URLs
            if not rel_path.endswith('/'):
                rel_path += '/'
            return f"/media/{rel_path}index.html"
        return None
