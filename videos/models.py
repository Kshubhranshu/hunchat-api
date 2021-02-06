from django.db import models


class Video(models.Model):
    """
    Video model instance.
    """

    file = models.FileField(
        upload_to="videos",
        blank=False,
        null=True,
    )
