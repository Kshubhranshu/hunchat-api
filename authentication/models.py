from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model.
    """

    first_name = None
    last_name = None
    name = models.CharField(null=False, blank=False, max_length=50)

    email = models.EmailField(unique=True, null=False, blank=False)
    is_email_verified = models.BooleanField(default=False)

    # profile image
    image = models.ImageField(upload_to="images", null=True, blank=True)

    bio = models.CharField(null=True, blank=True, max_length=200)
    bio_video = models.ForeignKey(
        "videos.Video",
        related_name="user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    location = models.CharField(null=True, blank=True, max_length=40)

    link = models.URLField(null=True, blank=True)

    are_terms_accepted = models.BooleanField(default=False)

    is_newsletter_subscribed = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "name",
        "email",
    ]

    class Meta:
        ordering = ["-date_joined"]

    @classmethod
    def is_username_taken(cls, username):
        users = cls.objects.filter(username=username)
        if not users.exists():
            return False
        return True

    @classmethod
    def is_email_taken(cls, email):
        try:
            cls.objects.get(email=email)
            return True
        except User.DoesNotExist:
            return False
