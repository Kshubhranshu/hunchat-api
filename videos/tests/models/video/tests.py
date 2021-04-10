from django.test import TestCase

from videos.models import Video


class VideoTests(TestCase):
    fixtures = ["users.json", "videos.json"]
