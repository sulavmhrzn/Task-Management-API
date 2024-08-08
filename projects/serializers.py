from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
            "priority",
            "budget",
            "team",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by"]

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError(
                {"end_date": "The end date should be before start date."}
            )
        return super().validate(attrs)
