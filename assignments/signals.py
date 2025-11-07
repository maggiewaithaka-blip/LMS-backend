from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='assignments.Submission')
def enqueue_grading_on_create(sender, instance, created, **kwargs):
    """When a Submission is created, enqueue the grading task if it has no grade.

    We import models and the Celery task inside the handler to avoid app
    loading/circular import issues at module import time.
    """
    if not created:
        return

    try:
        # local imports to avoid circular import problems
        from .models import AssignmentGrade
        from .tasks import grade_submission_task

        # Only enqueue if a grade does not yet exist for this submission
        if not hasattr(instance, 'grade'):
            grade_submission_task.delay(instance.id)
    except Exception:
        # Never raise from a signal handler in production code; log instead.
        # For now, swallow exceptions to avoid breaking the request flow.
        pass
