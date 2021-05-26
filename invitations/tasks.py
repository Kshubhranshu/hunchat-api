from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from celery import shared_task


@shared_task
def send_welcome_to_waiting_list_mail(email):
    pass
