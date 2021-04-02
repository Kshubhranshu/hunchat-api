from django.urls import include, path, reverse
from django.contrib.auth.hashers import check_password
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

from authentication.models import User


class UserViewSetTests(APITestCase, URLPatternsTestCase):
    fixtures = ["users.json"]
    urlpatterns = [
        path("api/", include("authentication.urls")),
    ]

    def test_create_user_list_endpoint(self):
        url = reverse("authentication:user-list")
        self.assertEqual(url, "/api/users/")

    def test_create_user_missing_required_fields(self):
        """
        Ensure we cannot create a new user object with missing required fields.
        """
        url = reverse("authentication:user-list")
        response = self.client.post(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["username"],
            [ErrorDetail(string="This field is required.", code="required")],
        )
        self.assertEqual(
            response.data["name"],
            [ErrorDetail(string="This field is required.", code="required")],
        )
        self.assertEqual(
            response.data["email"],
            [ErrorDetail(string="This field is required.", code="required")],
        )
        self.assertEqual(
            response.data["password"],
            [ErrorDetail(string="This field is required.", code="required")],
        )

    def test_create_user_username_taken(self):
        """
        Ensure we cannot create a new user object with a username already taken.
        """
        url = reverse("authentication:user-list")
        data = {
            "name": "Rachel Carson",
            "username": "marie",
            "email": "rcarson@jhu.edu",
            "password": "sdlk#j6920n12!",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["username"],
            [
                ErrorDetail(
                    string="A user with that username already exists.", code="unique"
                )
            ],
        )

    def test_create_user_email_taken(self):
        """
        Ensure we cannot create a new user object with an email already taken.
        """
        url = reverse("authentication:user-list")
        data = {
            "name": "Lise Meitner",
            "username": "lise",
            "email": "charles@hmsbeagle.com",
            "password": "3kjf9l1adjkl",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["email"],
            [ErrorDetail(string="user with this email already exists.", code="unique")],
        )

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse("authentication:user-list")
        data = {
            "name": "Sally Ride",
            "username": "astrosally",
            "email": "sride@nasa.gov",
            "password": "slkaj&#azk!",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 7)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["username"], data["username"])
        self.assertEqual(response.data["email"], data["email"])
        self.assertTrue(check_password(data["password"], response.data["password"]))
        self.assertFalse(check_password("slkd&12@", response.data["password"]))
        self.assertFalse(response.data["are_terms_accepted"])
        self.assertFalse(response.data["is_newsletter_subscribed"])
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(username="astrosally").name, "Sally Ride")

    def test_partial_update_user_name(self):
        """
        Ensure we can partially update a user object's name field.
        """
        user = User.objects.get(username="charles")
        lookup = external_id_from_model_and_internal_id(User, user.pk)
        url = reverse("authentication:user-detail", kwargs={"pk": lookup})
        data = {"name": "Charles Robert Darwin"}

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.patch(url, data, format="json")

        user = User.objects.get(username="charles")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.name, data["name"])

    def test_partial_update_user_username(self):
        """
        Ensure we can partially update a user object's username field.
        """
        user = User.objects.get(username="charles")
        lookup = external_id_from_model_and_internal_id(User, user.pk)
        url = reverse("authentication:user-detail", kwargs={"pk": lookup})
        data = {"username": "darwinzinho"}

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.patch(url, data, format="json")

        user = User.objects.get(pk=user.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.username, data["username"])
