from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "priority",
        "budget",
        "created_by",
        "start_date",
        "end_date",
        "get_assigned_team_members",
    ]
    list_filter = [
        "priority",
    ]

    @admin.display(description="team members")
    def get_assigned_team_members(self, obj):
        return ", ".join([member.username for member in obj.team.all()])
