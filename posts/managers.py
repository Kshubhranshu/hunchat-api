from django.db import models

from hunchat.model_loaders import (
    get_post_comment_notification_model,
    get_post_like_notification_model,
)


class PostManager(models.Manager):
    def create(self, *args, **kwargs):
        post = super(PostManager, self).create(*args, **kwargs)

        comment_to = kwargs.get("comment_to", None)
        if comment_to:
            # create PostCommentNotification if post is a comment
            PostCommentNotification = get_post_comment_notification_model()
            PostCommentNotification.objects.create(
                owner_id=comment_to.author.id, post_comment=post
            )

        return post


class PostLikeManager(models.Manager):
    def create(self, *args, **kwargs):
        post_like = super(PostManager, self).create(*args, **kwargs)

        post_author = kwargs.get("post").author

        PostLikeNotification = get_post_like_notification_model()
        PostLikeNotification.objects.create(
            owner_id=post_author.id, post_like=post_like
        )

        return post_like
