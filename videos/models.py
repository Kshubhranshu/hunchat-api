from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()
VideoCommentNotification = get_video_comment_notification_model()


class VideoManager(models.Manager):
    def create(self, *args, **kwargs):
        video = super(VideoManager, self).create(*args, **kwargs)

        if kwargs["answer_to"]:
            # create VideoCommentNotification if video is a comment
            VideoCommentNotification.objects.create(
                owner_id=answer_to.id, video_comment=video
            )

        return video


class Video(models.Model):
    """
    Video model instance.
    """

    description = models.CharField(
        blank=True, max_length=settings.VIDEO_DESCRIPTION_MAX_LENGTH
    )
    file = models.FileField(
        upload_to="videos",
        blank=False,
        null=True,
    )
    resources_link = models.URLField()
    author = models.ForeignKey(User, related_name="videos", on_delete=models.CASCADE)

    # If video is a comment, this field represents the video it is commenting on.
    answer_to = models.ForeignKey(
        Video, related_name="comments", on_delete=models.CASCADE
    )

    objects = VideoManager()
