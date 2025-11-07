# eccgd_backend package
# Ensure the Celery app is always imported when Django starts so shared_task
# decorated tasks will be registered.
from .celery import app as celery_app  # noqa

__all__ = ('celery_app',)
