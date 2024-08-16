from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "applications.tasks"

    def ready(self):
        import applications.tasks.signals
