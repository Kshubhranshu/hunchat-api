from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model


User = get_user_model()


class Notification(models.Model):
    owner = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False)
    unread = models.BooleanField(default=True)

    VIDEO_COMMENT = 'VC'

    NOTIFICATION_TYPES = (
        (VIDEO_COMMENT, 'Video Comment'),
    )

    notification_type = models.CharField(max_length=3, choices=NOTIFICATION_TYPES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class VideoCommentNotification(models.Model):
    notification = GenericRelation(Notification)
    video_comment = models.ForeignKey(VideoComment, on_delete=models.CASCADE)
