from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()


class Video(models.Model):
    """
    Video model instance.
    """
    description = models.CharField(blank=True, max_length=settings.VIDEO_DESCRIPTION_MAX_LENGTH)
    file = models.FileField(upload_to='videos', blank=False, null=True,)
    resources_link = models.URLField()
    author = models.ForeignKey(User, related_name='videos', on_delete=models.CASCADE)
