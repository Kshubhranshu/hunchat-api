from io import BytesIO

from django.db import models
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

import cv2


class VideoManager(models.Manager):
    """
    Video model manager.
    """

    def create(self, *args, **kwargs):
        video = super(VideoManager, self).create(*args, **kwargs)

        vidcap = cv2.VideoCapture(video.file.url)
        success, frame = vidcap.read()
        if success:
            success_, image = cv2.imencode(".jpeg", frame)
            buffer = BytesIO(image)
            poster = ContentFile(buffer.getvalue())
            poster_field = video.poster
            poster_name = "poster-{}.jpeg".format(video.pk)
            poster_field.save(
                poster_name,
                InMemoryUploadedFile(
                    poster, None, poster_name, "image/jpeg", poster.tell, None
                ),
            )

        return video
