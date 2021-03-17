from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string


class Invitation(models.Model):
    email = models.EmailField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.send_invite_email(email=self.email)
        return super(Invitation, self).save(*args, **kwargs)

    def send_invite_email(self, email):
        subject = "Welcome to Hunchat"
        text_content = render_to_string("invitations/email/welcome_waiting_list.txt")
        html_content = render_to_string("invitations/email/welcome_waiting_list.html")
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            from_email="Hunchat Team <{0}>".format(settings.DEFAULT_FROM_EMAIL),
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
