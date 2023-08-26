from django.conf import settings
from django.core.mail import send_mail

from config import celery_app

WELCOME_MESSAGE_SUBJECT = "Welcome to our project"
WELCOME_MESSAGE_TEXT = "Thank you for registration!"


@celery_app.task
def send_welcome_message(email: str):
    """Send welcome message task."""
    send_mail(
        WELCOME_MESSAGE_SUBJECT,
        WELCOME_MESSAGE_TEXT,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
