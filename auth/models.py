import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    email = models.EmailField(unique=True, null=False, blank=False)
    is_email_verified = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email',]
