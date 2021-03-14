from io import BytesIO

from django.db import models
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image

from cv2 import VideoCapture


class VideoManager(models.Manager):
    """
    Video model manager.
    """

    def create(self, *args, **kwargs):
        video = super(VideoManager, self).create(*args, **kwargs)

        vidcap = VideoCapture(video.file.url)
        success, frame = vidcap.read()
        if success:
            image = Image.fromarray(frame)
            buffer = BytesIO()
            image.save(fp=buffer, format="jpeg")
            poster = ContentFile(buffer.getvalue())
            poster_field = video.poster
            poster_name = "poster-{}.jpeg".format(video.pk)
            poster_field.save(poster_name, InMemoryUploadedFile(
                poster,
                None,
                poster_name,
                "image/jpeg",
                poster.tell,
                None
            ))

        return video
