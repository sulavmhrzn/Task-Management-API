from django.contrib import admin

from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "task_type",
        "status",
        "priority",
        "created_by",
        "project",
        "get_assigned_developers",
    ]
    list_filter = ["status", "task_type", "priority", "project"]

    @admin.display(description="assigned developers")
    def get_assigned_developers(self, obj):
        return ", ".join(
            [developer.username for developer in obj.assigned_developers.all()]
        )
