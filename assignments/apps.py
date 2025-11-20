from django.apps import AppConfig


class AssignmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assignments'

    def ready(self):
        # Import signal handlers to ensure they're registered when the app is ready
        try:
            import assignments.signals  # noqa
        except Exception:
            # Avoid breaking app startup in case of import errors during development
            pass
