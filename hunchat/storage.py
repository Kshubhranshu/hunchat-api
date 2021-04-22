import uuid
import os

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class S3StaticStorage(S3Boto3Storage):
    """
    Storage class for static files.
    """

    location = settings.AWS_STATIC_LOCATION


class S3MediaStorage(S3Boto3Storage):
    """
    Storage class for media files.
    """

    location = settings.AWS_MEDIA_LOCATION


def get_video_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("videos/", filename)


def get_image_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("images/", filename)
