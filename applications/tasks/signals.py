from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed, post_save, pre_delete, pre_save
from django.dispatch import receiver

from .models import AuditLog, Task

User = get_user_model()


@receiver(pre_save, sender=Task)
def capture_previous_state(sender, instance, **kwargs):
    if instance.pk:
        try:
            existing_task = Task.objects.get(pk=instance.pk)
            instance._previous_state = {
                "title": existing_task.title,
                "description": existing_task.description,
                "status": existing_task.status,
                "task_type": existing_task.task_type,
                "priority": existing_task.priority,
                "project": existing_task.project.pk,
            }
        except Task.DoesNotExist:
            instance._previous_state = None
    else:
        instance._previous_state = None


@receiver(m2m_changed, sender=Task.assigned_developers.through)
def track_assigned_developers_changes(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        if not hasattr(instance, "_previous_state") or instance._previous_state is None:
            instance._previous_state = {
                "assigned_developers": list(
                    instance.assigned_developers.values_list("username", flat=True)
                )
            }
        previous_state = getattr(instance, "_previous_state", None)
        print("M2M: ", previous_state)
        current_developers = set(
            instance.assigned_developers.values_list("username", flat=True)
        )
        previous_developers = (
            set(previous_state["assigned_developers"]) if previous_state else set()
        )

        if previous_state and current_developers != previous_developers:
            changed_fields = {
                "assigned_developers": {
                    "old_value": list(previous_developers),
                    "new_value": list(current_developers),
                }
            }

            AuditLog.objects.create(
                user=instance.created_by,
                action_type="update",
                task=instance,
                changed_fields=changed_fields,
                previous_state=previous_state,
                description="Assigned developers updated",
            )
        instance._previous_state["assigned_developers"] = list(current_developers)


@receiver(post_save, sender=Task)
def create_audit_log(sender, instance, created, **kwargs):
    if not hasattr(instance, "_previous_state") or instance._previous_state is None:
        instance._previous_state = {
            "title": instance.title,
            "description": instance.description,
            "status": instance.status,
            "task_type": instance.task_type,
            "priority": instance.priority,
            "project": instance.project.pk,
            "assigned_developers": list(
                instance.assigned_developers.values_list("username", flat=True)
            ),
        }

    previous_state = instance._previous_state
    print("Current: ", instance._previous_state)
    changed_fields = {}

    if created:
        action_type = "create"
        previous_state = None
    else:
        action_type = "update"
        current_state = {
            "title": instance.title,
            "description": instance.description,
            "status": instance.status,
            "task_type": instance.task_type,
            "priority": instance.priority,
            "project": instance.project.pk,
        }
        for field, old_value in previous_state.items():
            if field != "assigned_developers":  # Handled separately in m2m_changed
                new_value = current_state[field]
                if old_value != new_value:
                    changed_fields[field] = {
                        "old_value": old_value,
                        "new_value": new_value,
                    }

        # Update _previous_state after post_save
        instance._previous_state.update(current_state)
        instance._previous_state["assigned_developers"] = list(
            instance.assigned_developers.values_list("username", flat=True)
        )
    AuditLog.objects.create(
        user=instance.created_by,
        action_type=action_type,
        task=instance,
        changed_fields=changed_fields if changed_fields else None,
        previous_state=previous_state if previous_state else None,
        description=f"Task {action_type}",
    )


@receiver(pre_delete, sender=Task)
def log_task_deletion(sender, instance, **kwargs):
    AuditLog.objects.create(
        user=instance.created_by,
        action_type="delete",
        task=instance,
        previous_state={
            "title": instance.title,
            "description": instance.description,
            "status": instance.status,
            "task_type": instance.task_type,
            "priority": instance.priority,
            "project": instance.project.pk,
        },
        description="Task deleted",
    )
