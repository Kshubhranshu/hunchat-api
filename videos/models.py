from django.db import models

from hunchat.storage import get_video_file_path, get_image_file_path

from videos.managers import VideoManager


class Video(models.Model):
    """
    Video model instance.
    """

    file = models.FileField(
        upload_to=get_video_file_path,
        blank=False,
        null=False,
    )
    duration = models.DecimalField(
        max_digits=19, decimal_places=10, null=False, blank=False
    )  # duration in seconds
    height = models.PositiveIntegerField()  # height in pixels
    width = models.PositiveIntegerField()  # width in pixels

    poster = models.ImageField(
        upload_to=get_image_file_path,
        height_field="poster_height",
        width_field="poster_width",
        blank=True,
        null=True,
    )
    poster_height = models.PositiveIntegerField(
        blank=True, null=True
    )  # height in pixels
    poster_width = models.PositiveIntegerField(blank=True, null=True)  # width in pixels

    objects = VideoManager()
