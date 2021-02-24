from django.db import models


class Video(models.Model):
    """
    Video model instance.
    """

    file = models.FileField(
        upload_to="videos",
        blank=False,
        null=False,
    )
    duration = models.DecimalField(
        max_digits=19, decimal_places=10, null=False, blank=False
    )  # duration in seconds
    height = models.PositiveIntegerField()  # height in pixels
    width = models.PositiveIntegerField()  # width in pixels
