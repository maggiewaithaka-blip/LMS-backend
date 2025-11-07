from django.db import models


class CourseResource(models.Model):
    RESOURCE_TYPES = (
        ('file', 'File'),
        ('url', 'URL'),
        ('page', 'Page'),
    )
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    # link to storage.File when resource_type == 'file'
    file = models.ForeignKey('storage.File', null=True, blank=True, on_delete=models.SET_NULL)
    url = models.URLField(blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_download_url(self):
        if self.resource_type == 'file' and self.file:
            return self.file.get_download_url()
        if self.resource_type == 'url' and self.url:
            return self.url
        return None

    def __str__(self):
        return f"[{self.course}] {self.title}"
