from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_create_task_mail(task):
    developers = task.assigned_developers.all()
    emails = [dev.email for dev in developers]

    html_message = render_to_string(
        template_name="task_create_email.html",
        context={
            "project_name": task.project,
            "task_title": task.title,
            "task_description": task.description,
            "assigned_by": task.created_by,
            "priority_level": task.priority,
        },
    )
    plain_text_message = strip_tags(html_message)

    send_mail(
        subject=f"New Task Assigned: {task.title}",
        message=plain_text_message,
        html_message=html_message,
        from_email="admin@task.com",
        recipient_list=emails,
    )
