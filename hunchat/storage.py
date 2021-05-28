from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class S3StaticStorage(S3Boto3Storage):
    """
    Storage class for static files.
    """

    bucket_name = settings.AWS_STORAGE_STATIC_BUCKET_NAME


class S3InputMediaStorage(S3Boto3Storage):
    """
    Storage class for uploading media files.
    """

    bucket_name = settings.AWS_STORAGE_MEDIA_INPUT_BUCKET_NAME



