from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Goal


@shared_task
def send_goal_confirmation_email(goal_id: int, user_email):
    goal = Goal.objects.filter(id=goal_id).first()

    subject = "Goal Submission Confirmation"
    message = f"Your Goal: {goal.title} has been received and is being processed."
    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])


@shared_task
def check_profanity(text: str) -> bool:
    pass
