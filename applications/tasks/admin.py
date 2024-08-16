import json

from django.contrib import admin
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import JsonLexer

from .models import AuditLog, Task


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


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    readonly_fields = ("changed_fields_prettified", "previous_state_prettified")

    def changed_fields_prettified(self, instance):
        print(instance.changed_fields)
        response = json.dumps(instance.changed_fields, sort_keys=True, indent=2)
        response = response[:5000]
        formatter = HtmlFormatter(style="colorful")
        response = highlight(response, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style>"
        return mark_safe(style + response)

    def previous_state_prettified(self, instance):
        response = json.dumps(instance.previous_state, sort_keys=True, indent=2)
        response = response[:5000]
        formatter = HtmlFormatter(style="colorful")
        response = highlight(response, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style>"
        return mark_safe(style + response)
