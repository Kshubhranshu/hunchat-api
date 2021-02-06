from django.db import models
from django.conf import settings


class PostManager(models.Manager):
    def create(self, *args, **kwargs):
        post = super(PostManager, self).create(*args, **kwargs)

        if kwargs["answer_to"]:
            # create PostCommentNotification if post is a comment
            PostCommentNotification = get_post_comment_notification_model()
            PostCommentNotification.objects.create(
                owner_id=answer_to.id, post_comment=post
            )

        return post


class Post(models.Model):
    description = models.CharField(
        blank=True, max_length=settings.POST_DESCRIPTION_MAX_LENGTH
    )
    video = models.ForeignKey(
        "videos.Video", related_name="post", on_delete=models.CASCADE
    )
    resources_link = models.URLField()
    author = models.ForeignKey(
        "authentication.User", related_name="posts", on_delete=models.CASCADE
    )
    answer_to = models.ForeignKey(
        "posts.Post", related_name="comments", on_delete=models.CASCADE
    )

    objects = PostManager()
