from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from celery import shared_task


@shared_task
def send_confirm_email_mail(email):
    pass


@shared_task
def send_welcome_mail(email):
    pass
