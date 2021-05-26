from django.db.models.signals import post_save
from django.dispatch import receiver

from django_rq import enqueue

from videos.tasks import create_poster
from videos.models import Video


@receiver(post_save, sender=Video)
def create_poster(sender, instance, **kwargs):
    enqueue(tasks.create_poster, instance.pk)
