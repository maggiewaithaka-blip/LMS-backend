from django.db import models


class Attachment(models.Model):
    ATTACHMENT_TYPES = (
        ('pdf', 'PDF'),
        ('link', 'Link'),
        ('text', 'Text'),
    )
    type = models.CharField(max_length=10, choices=ATTACHMENT_TYPES)
    file = models.FileField(upload_to='attachments/', null=True, blank=True)
    url = models.URLField(blank=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type}: {self.file or self.url or self.text[:30]}"

class Attachment(models.Model):
    ATTACHMENT_TYPES = (
        ('pdf', 'PDF'),
        ('link', 'Link'),
        ('text', 'Text'),
    )
    type = models.CharField(max_length=10, choices=ATTACHMENT_TYPES)
    file = models.FileField(upload_to='attachments/', null=True, blank=True)
    url = models.URLField(blank=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type}: {self.file or self.url or self.text[:30]}"

from django.db import models
from django.conf import settings


