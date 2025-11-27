from django.db import models



class Attachment(models.Model):
    ATTACHMENT_TYPES = (
        ('pdf', 'PDF'),
        ('link', 'Link'),
        ('text', 'Text'),
        ('video', 'Video'),
        ('audio', 'Audio'),
    )
    type = models.CharField(max_length=10, choices=ATTACHMENT_TYPES)
    file = models.FileField(upload_to='attachments/', null=True, blank=True, help_text='Upload PDF, video, audio, or other files')
    url = models.URLField(blank=True, help_text='Add a link for web resources, videos, etc.')
    text = models.TextField(blank=True, help_text='Add text content if needed')
    created_at = models.DateTimeField(auto_now_add=True)

    assignment = models.ForeignKey('courses.Assignment', on_delete=models.CASCADE, null=True, blank=True, related_name='attachments')
    quiz = models.ForeignKey('courses.Quiz', on_delete=models.CASCADE, null=True, blank=True, related_name='attachments')
    resource = models.ForeignKey('courses.Resource', on_delete=models.CASCADE, null=True, blank=True, related_name='attachments')

    def __str__(self):
        return f"{self.type}: {self.file or self.url or self.text[:30]}"