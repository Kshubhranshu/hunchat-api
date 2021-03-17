from django.conf import settings
from django.db import models

from posts.managers import PostLikeManager, PostManager


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
    created_at = models.DateTimeField(auto_now_add=True)
    comment_to = models.ForeignKey(
        "posts.Post",
        related_name="comments",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    objects = PostManager()

    class Meta:
        ordering = ["-created_at"]

    def get_comments(self):
        return self.comments

    def get_comments_count(self):
        return self.get_comments().count()

    def get_likes(self):
        return self.likes

    def get_likes_count(self):
        return self.get_likes().count()

    def get_thread(self):
        if self.comment_to:
            thread = [self]
            next_post_up = self.comment_to
            while next_post_up:
                thread.insert(0, next_post_up)
                next_post_up = next_post_up.comment_to
            return thread
        return None


class PostLike(models.Model):
    user = models.ForeignKey(
        "authentication.User", related_name="likes", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        "posts.Post",
        related_name="likes",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    objects = PostLikeManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_like")
        ]
