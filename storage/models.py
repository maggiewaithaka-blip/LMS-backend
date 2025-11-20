from django.db import models
from django.conf import settings


class File(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='files')
    file = models.FileField(upload_to='uploads/')
    filename = models.CharField(max_length=512)
    content_type = models.CharField(max_length=255, blank=True)
    size = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    def get_download_url(self, expires_in=3600):
        """Return a signed URL for downloading this file when S3 is configured,
        otherwise return the storage URL.
        """
        try:
            import boto3
            from django.conf import settings
            # Require AWS settings
            aws_bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
            if aws_bucket and self.file.name:
                client = boto3.client('s3',
                                      aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID', None),
                                      aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
                                      region_name=getattr(settings, 'AWS_S3_REGION_NAME', None))
                key = self.file.name
                url = client.generate_presigned_url('get_object', Params={'Bucket': aws_bucket, 'Key': key}, ExpiresIn=expires_in)
                return url
        except Exception:
            pass

        # Fallback: use storage url (works for local dev)
        try:
            return self.file.url
        except Exception:
            return None
