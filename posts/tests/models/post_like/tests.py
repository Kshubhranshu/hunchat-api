from django.test import TestCase

from posts.models import PostLike


class PostLikeTests(TestCase):
    fixtures = ["users.json", "videos.json", "posts.json", "post_likes.json"]
