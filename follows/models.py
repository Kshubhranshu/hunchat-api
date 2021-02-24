from django.db import models


class Follow(models.Model):
    list = models.ForeignKey(
        "lists.List", related_name="follower", on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        "authentication.User", related_name="followed", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "followed"], name="unique_follow"
            )
        ]
