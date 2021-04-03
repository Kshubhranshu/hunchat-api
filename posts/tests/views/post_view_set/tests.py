import json
from django.urls import include, path, reverse
from rest_framework.test import (
    APIClient,
    APITestCase,
    URLPatternsTestCase,
)
from rest_framework import status
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework_serializer_extensions.utils import (
    external_id_from_model_and_internal_id,
)

from posts.models import Post


class PostViewSetTests(APITestCase, URLPatternsTestCase):
    fixtures = ["users.json", "videos.json", "posts.json", "post_likes.json"]
    urlpatterns = [
        path("api/", include("posts.urls")),
    ]

    def test_post_list_endpoint(self):
        url = reverse("posts:post-list")
        self.assertEqual(url, "/api/posts/")

    def test_post_list(self):
        """
        Ensure we can list all posts.
        """
        url = reverse("posts:post-list")
        response = self.client.get(url, format="json")

        self.assertEqual(len(response.data["results"]), 10)

    def test_post_detail(self):
        """
        Ensure we can retrieve a post detail.
        """
        lookup = external_id_from_model_and_internal_id(Post, 1)
        url = reverse("posts:post-detail", kwargs={"pk": lookup})
        response = self.client.get(url, format="json")

        self.assertEqual(
            json.loads(response.content),
            {
                "id": "d6Vzm4T4nY9R",
                "description": "All about this week's tour",
                "video": {
                    "id": 1,
                    "file": "https://hunchat-assets.s3-accelerate.amazonaws.com/media/videos/XXXX.MOV",
                    "file_url": "https://hunchat-assets.s3-accelerate.amazonaws.com/media/videos/XXXX.MOV",
                    "duration": "32.3650000000",
                    "height": 1920,
                    "width": 1080,
                    "poster": "https://hunchat-assets.s3-accelerate.amazonaws.com/media/images/XXXX.jpeg",
                    "poster_url": "https://hunchat-assets.s3-accelerate.amazonaws.com/media/images/XXXX.jpeg",
                    "poster_height": 1920,
                    "poster_width": 1080,
                },
                "resources_link": "",
                "author": {
                    "id": "bGPn5RUZzeqo",
                    "username": "marie",
                    "name": "Marie Curie",
                    "email": "marie@u-paris.fr",
                    "image": None,
                    "image_url": None,
                    "bio": None,
                    "bio_video": None,
                    "location": None,
                    "date_joined": "2021-02-01T22:54:07.871791Z",
                    "link": None,
                },
                "created_at": "2021-02-22T15:36:40.982000Z",
                "comment_to": None,
                "comments": [
                    {
                        "id": "raW7e4TKzNB1",
                        "video": {
                            "id": 6,
                            "file": "https://hunchat-assets.s3-accelerate.amazonaws.com/media/videos/XXXX.MOV",
                            "file_url": "https://hunchat-assets.s3-accelerate.amazonaws.com/media/videos/XXXX.MOV",
                            "duration": "15.9601654667",
                            "height": 1920,
                            "width": 1080,
                            "poster": "https://hunchat-assets.s3-accelerate.amazonaws.com/media/images/XXXX.jpeg",
                            "poster_url": "https://hunchat-assets.s3-accelerate.amazonaws.com/media/images/XXXX.jpeg",
                            "poster_height": 1920,
                            "poster_width": 1080,
                        },
                        "author": {
                            "id": "kVe70xU67A8Y",
                            "username": "charles",
                            "name": "Charles Darwin",
                            "email": "charles@hmsbeagle.com",
                            "image": None,
                            "image_url": None,
                            "bio": None,
                            "bio_video": None,
                            "location": None,
                            "date_joined": "2021-02-01T21:54:07.871791Z",
                            "link": None,
                        },
                    },
                    {
                        "id": "k9egBrTdgXAr",
                        "video": {
                            "id": 2,
                            "file": "https://hunchat-assets.s3-accelerate.amazonaws.com/media/videos/XXXX.MOV",
                            "file_url": "https://hunchat-assets.s3-accelerate.amazonaws.com/media/videos/XXXX.MOV",
                            "duration": "8.4616235667",
                            "height": 1920,
                            "width": 1080,
                            "poster": "https://hunchat-assets.s3-accelerate.amazonaws.com/media/images/XXXX.jpeg",
                            "poster_url": "https://hunchat-assets.s3-accelerate.amazonaws.com/media/images/XXXX.jpeg",
                            "poster_height": 1920,
                            "poster_width": 1080,
                        },
                        "author": {
                            "id": "kVe70xU67A8Y",
                            "username": "charles",
                            "name": "Charles Darwin",
                            "email": "charles@hmsbeagle.com",
                            "image": None,
                            "image_url": None,
                            "bio": None,
                            "bio_video": None,
                            "location": None,
                            "date_joined": "2021-02-01T21:54:07.871791Z",
                            "link": None,
                        },
                    },
                ],
                "comments_count": 2,
                "likes": [
                    {"id": "k9egBqCM7XAr", "user": {"id": "kVe70xU67A8Y"}},
                    {"id": "3QEzvRCBzp51", "user": {"id": "dKx72LUpn64G"}},
                ],
                "likes_count": 2,
            },
        )
