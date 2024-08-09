from django.contrib.auth import get_user_model
from django.db import models

from projects.models import Project

User = get_user_model()


class Task(models.Model):
    class TASK_TYPE(models.TextChoices):
        BUG = "Bug"
        FEATURE_REQUEST = "Feature Request"
        TODO = "Todo"
        CUSTOMER_SUPPORT = "Customer Support"

    class STATUS(models.TextChoices):
        OPEN = "Open"
        IN_PROGRESS = "In Progress"
        CLOSED = "Closed"

    class PRIORITY(models.TextChoices):
        HIGH = "High"
        MEDIUM = "Medium"
        LOW = "Low"

    title = models.CharField(max_length=255)
    description = models.TextField()
    task_type = models.CharField(
        max_length=255, choices=TASK_TYPE.choices, default=TASK_TYPE.TODO
    )
    status = models.CharField(
        max_length=255, choices=STATUS.choices, default=STATUS.OPEN
    )
    priority = models.CharField(
        max_length=255, choices=PRIORITY.choices, default=PRIORITY.LOW
    )
    created_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="tasks"
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_developers = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["title"])]

    def __str__(self):
        return self.title
