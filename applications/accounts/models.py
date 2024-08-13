from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class ROLE(models.TextChoices):
        MANAGER = "manager"
        DEVELOPER = "developer"

    role = models.CharField(max_length=255, choices=ROLE.choices, default=ROLE.MANAGER)

    def is_manager(self):
        return self.role == self.ROLE.MANAGER

    def is_developer(self):
        return self.role == self.ROLE.DEVELOPER
