from django.db import models


class List(models.Model):
    name = models.CharField(max_length=20)
    tag = models.SlugField()
    owner = models.ForeignKey(
        "authentication.User", related_name="lists", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
