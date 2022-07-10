from celery import shared_task
from django.core.mail import send_mail
from privetNote import settings


@shared_task(name="send_feedback_email_task")
def send_feedback_email_task(subject,message,email):
    """sends an email when feedback form is filled successfully"""
    return send_mail(subject, message, settings.EMAIL_HOST, [email])