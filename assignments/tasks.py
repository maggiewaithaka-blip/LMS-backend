from celery import shared_task
from django.utils import timezone


@shared_task(bind=True)
def grade_submission_task(self, submission_id):
    """Simple example task: mark a submission as graded with a default score.

    In a real app this would run autograding logic (MCQ marking, plagiarism checks,
    calling external graders, etc.). This example demonstrates a background job
    that updates the database and returns a result payload.
    """
    try:
        # Import here to avoid issues when Celery loads module before Django apps ready
        from .models import Submission, AssignmentGrade

        submission = Submission.objects.get(id=submission_id)

        # Example auto-grade: set a fixed score and feedback
        grade, _ = AssignmentGrade.objects.get_or_create(submission=submission)
        grade.score = 100
        grade.feedback = 'Auto-graded by sample Celery task.'
        grade.grader = None
        grade.save()

        return {
            'submission_id': submission_id,
            'score': float(grade.score) if grade.score is not None else None,
            'graded_at': timezone.now().isoformat(),
        }
    except Submission.DoesNotExist:
        return {'error': 'submission_not_found', 'submission_id': submission_id}
    except Exception as exc:
        # Use Celery retry semantics if desired; for now return an error payload
        return {'error': 'exception', 'detail': str(exc)}


@shared_task(bind=True)
def periodic_grading_check(self):
    """Periodic task that finds ungraded submissions and enqueues grading jobs.

    This is intentionally conservative: it only enqueues a grading task for
    submissions that don't yet have an AssignmentGrade.
    """
    try:
        from .models import Submission, AssignmentGrade

        ungraded = Submission.objects.filter(grade__isnull=True).order_by('submitted_at')[:100]
        count = 0
        for sub in ungraded:
            # Enqueue the per-submission grading task
            grade_submission_task.delay(sub.id)
            count += 1

        return {'enqueued': count}
    except Exception as exc:
        return {'error': 'exception', 'detail': str(exc)}
