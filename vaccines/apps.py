from django.apps import AppConfig


class VaccinesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vaccines"

    def ready(self):
        import vaccines.signals