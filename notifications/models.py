from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    owner = models.ForeignKey(
        "authentication.User", related_name="notifications", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(editable=False)
    unread = models.BooleanField(default=True)

    POST_COMMENT = "PC"

    NOTIFICATION_TYPES = ((POST_COMMENT, "Post Comment"),)

    notification_type = models.CharField(max_length=3, choices=NOTIFICATION_TYPES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class PostCommentNotificationManager(models.Manager):
    def create(self, *args, **kwargs):
        post_comment_notification = super(PostCommentNotificationManager, self).create(
            *args, **kwargs
        )
        Notification.objects.create(
            owner_id=kwargs["owner_id"],
            notification_type=Notification.POST_COMMENT,
            content_object=post_comment_notification,
        )
        return post_comment_notification


class PostCommentNotification(models.Model):
    notification = GenericRelation("notifications.Notification")
    post_comment = models.ForeignKey("posts.Post", on_delete=models.CASCADE)

    objects = PostCommentNotificationManager()
