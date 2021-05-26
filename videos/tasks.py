from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image

from cv2 import VideoCapture

from videos.models import Video


def create_poster(pk):
    """Create videos.Video poster.

    Keyword arguments:
    pk -- videos.Video instance primary key (default None)
    """
    video = Video.objects.get(pk=pk)

    vidcap = VideoCapture(video.file.url)
    success, frame = vidcap.read()
    if success:
        image = Image.fromarray(frame)
        buffer = BytesIO()
        image.save(fp=buffer, format="jpeg")
        poster = ContentFile(buffer.getvalue())
        poster_field = video.poster
        poster_name = "poster-{}.jpeg".format(video.pk)
        poster_field.save(
            poster_name,
            InMemoryUploadedFile(
                poster, None, poster_name, "image/jpeg", poster.tell, None
            ),
        )

    ## IN CONSTRUCTION
