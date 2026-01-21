from django.db import models
import os




class ScormPackage(models.Model):
    section = models.ForeignKey("courses.CourseSection", on_delete=models.CASCADE, related_name='scorm_packages')
    name = models.CharField(max_length=255)
    zip_file = models.FileField(upload_to='scorm_zips/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Determine if a new zip file is being uploaded
        is_new = self.pk is None
        old_zip = None
        if not is_new:
            try:
                old = ScormPackage.objects.get(pk=self.pk)
                old_zip = old.zip_file
            except ScormPackage.DoesNotExist:
                pass
        super().save(*args, **kwargs)
        # Extract only if new or zip_file changed
        if is_new or (old_zip and old_zip != self.zip_file):
            self.extract_scorm_zip()

    def extract_scorm_zip(self):
        import zipfile, os
        if not self.zip_file:
            return
        extract_dir = os.path.join(os.path.dirname(self.zip_file.path), '..', 'scorm', f'scorm_{self.pk}')
        extract_dir = os.path.abspath(extract_dir)
        os.makedirs(extract_dir, exist_ok=True)
        try:
            with zipfile.ZipFile(self.zip_file.path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            # ...removed debug print...
        except Exception as e:
            pass

    def __str__(self):
        return self.name

    def get_extract_dir(self):
        # Directory where the SCORM package will be extracted
        return os.path.join('mediafiles', 'scorm', f'scorm_{self.pk}')

    @property
    def extracted_path(self):
        # Dynamically determine the extracted path (where index.html is found)
        import os
        extract_dir = os.path.join(os.path.dirname(self.zip_file.path), '..', 'scorm', f'scorm_{self.pk}')
        extract_dir = os.path.abspath(extract_dir)
        # ...removed debug print...
        if os.path.exists(extract_dir):
            for root, dirs, files in os.walk(extract_dir):
                # ...removed debug print...
                if 'index.html' in files:
                    # ...removed debug print...
                    return root
            # ...removed debug print...
            return extract_dir
        # ...removed debug print...
        return ''
