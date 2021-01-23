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
