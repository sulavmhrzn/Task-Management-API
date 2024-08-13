from rest_framework import serializers
from rest_framework.validators import ValidationError

from applications.projects.serializers import ProjectSerializer
from applications.tasks.serializers import TaskSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "role",
            "first_name",
            "last_name",
            "is_staff",
        )
        extra_kwargs = {"is_staff": {"write_only": True}}


class CreateUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        max_length=255, write_only=True, label="Confirm Password"
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "role",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, email):
        if not email:
            raise ValidationError("This field may not be blank")
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "email already in use",
            )
        return email

    def validate(self, attrs):
        password1 = attrs.get("password")
        password2 = attrs.get("password2")
        if password1 != password2:
            raise ValidationError("passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        instance = User.objects.create_user(**validated_data)
        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]

    def validate_email(self, data):
        user = User.objects.filter(email=data)
        if user.exists() and not user.first().id == self.instance.id:
            raise ValidationError("email already in use")
        return data


class DashboardSerializer(serializers.Serializer):
    user = UserSerializer()
    projects = ProjectSerializer(many=True)
    tasks = TaskSerializer(many=True)
