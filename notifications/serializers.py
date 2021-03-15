from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from rest_framework_serializer_extensions.fields import HashIdField

from generic_relations.relations import GenericRelatedField

from hunchat.model_loaders import (
    get_notification_model,
    get_post_comment_notification_model,
    get_post_like_notification_model,
)

from posts.serializers import PostCommentSerializer, PostLikeSerializer


class PostCommentNotificationSerializer(serializers.ModelSerializer):
    post_comment = PostCommentSerializer()

    class Meta:
        model = get_post_comment_notification_model()
        fields = ["post_comment"]


class NotificationSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    """
    Notification serializer with a `GenericRelatedField` mapping all possible
    notifications models to their respective serializers..
    """

    id = HashIdField(model=get_notification_model(), read_only=True)
    content_object = GenericRelatedField(
        {
            get_post_comment_notification_model(): PostCommentNotificationSerializer(),
        }
    )

    class Meta:
        model = get_notification_model()
        fields = ["id", "notification_type", "created_at", "unread", "content_object"]
