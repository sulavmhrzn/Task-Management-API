from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Project(models.Model):
    class PRIORITY(models.TextChoices):
        HIGH = "High"
        MEDIUM = "Medium"
        LOW = "Low"

    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    priority = models.CharField(
        max_length=255, choices=PRIORITY.choices, default=PRIORITY.LOW
    )
    budget = models.PositiveIntegerField()
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    team = models.ManyToManyField(
        User,
        related_name="projects",
        verbose_name="Team members",
        help_text="The team members assigned to this project",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError(
                {"end_date": "The end date should be before start date."}
            )
