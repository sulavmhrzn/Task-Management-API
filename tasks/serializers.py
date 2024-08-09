from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "task_type",
            "status",
            "priority",
            "project",
            "assigned_developers",
        ]

    def validate(self, attrs):
        request = self.context.get("request")
        current_user = request.user
        not_team_member = []

        if attrs["project"].created_by != current_user:
            raise serializers.ValidationError(
                {
                    "project": "You cannot create a task for a project you did not create."
                }
            )

        if not attrs.get("assigned_developer", None):
            for user in attrs["assigned_developers"]:
                # This might not be how I should filter it
                if user not in attrs["project"].team.all():
                    not_team_member.append(user.username)

        if not_team_member:
            raise serializers.ValidationError(
                {
                    "assigned_developers": f"{not_team_member} are not members of the team for this project."
                }
            )

        return super().validate(attrs)


class TaskUpdateSerializerForDeveloper(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["status", "priority", "task_type"]
        read_only_fields = ["title"]
