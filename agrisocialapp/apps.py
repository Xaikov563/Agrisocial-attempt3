from django.apps import AppConfig

class AgrisocialappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agrisocialapp'

    def ready(self):
        import agrisocialapp.signals  # Ensure signals are imported
