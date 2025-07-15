from django.apps import AppConfig


class MedicalTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medical_tracker'

    def ready(self):
        from . import signals  # noqa: F401
