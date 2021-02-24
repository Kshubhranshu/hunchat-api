from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from rest_framework_serializer_extensions.fields import HashIdField

from notifications.models import (
    Notification,
    PostCommentNotification,
    PostLikeNotification,
)

from posts.serializers import PostCommentSerializer, PostLikeSerializer


class NotificationContentObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `content_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serializer notification instances using specific notification type serializers.
        """
        if isinstance(value, PostCommentNotification):
            serializer = PostCommentSerializer(value)
            return serializer.data
        elif isinstance(value, PostLikeNotification):
            serializer = PostLikeSerializer(value)
            return serializer.data
        else:
            raise Exception(_("Unexpected type of notification object."))


class NotificationSerializer(serializers.ModelSerializer):
    """
    Notification serializer.
    """

    id = HashIdField(model=Notification, read_only=True)
    content_object = NotificationContentObjectRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "notification_type", "created_at", "unread", "content_object"]
