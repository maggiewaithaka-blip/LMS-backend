from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Attachment

@receiver(post_save, sender=Attachment)
def fix_nested_admin_file_issue(sender, instance, created, **kwargs):
    """
    Fix nested_admin not saving FileField on first attempt.
    When an Attachment is created via nested_admin, the file is not
    properly associated until the parent object exists.
    This forces a second save where Django writes the correct file path.
    """
    if created and instance.file:
        instance.save()
