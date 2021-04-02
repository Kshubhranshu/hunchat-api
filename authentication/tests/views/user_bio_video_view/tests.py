from django.urls import include, path
from rest_framework.test import (
    APITestCase,
    URLPatternsTestCase,
)


class UserBioVideoViewTests(APITestCase, URLPatternsTestCase):
    fixtures = ["users.json"]
    urlpatterns = [
        path("api/", include("authentication.urls")),
    ]

    def test_update_user_bio_video(self):
        """
        Ensure we can update a user's bio_video field.
        """
        pass
