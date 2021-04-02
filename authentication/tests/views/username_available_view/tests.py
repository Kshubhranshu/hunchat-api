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


class UsernameAvailableViewTests(APITestCase, URLPatternsTestCase):
    fixtures = ["users.json"]
    urlpatterns = [
        path("api/", include("authentication.urls")),
    ]

    def test_username_is_available(self):
        """
        Ensure we get a message indicating that a username is available for an available username.
        """
        url = reverse("authentication:username_available")
        data = {"username": "turing"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.data, {"username": "Username available."})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_username_is_not_available(self):
        """
        Ensure we get a message indicating that a username is NOT available for a username already in use.
        """
        url = reverse("authentication:username_available")
        data = {"username": "marie"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.data,
            {
                "username": [
                    ErrorDetail(string="The username is already taken.", code="invalid")
                ]
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_is_not_valid(self):
        """
        Ensure we get a message indicating that a username has invalid format for a username with invalid format.
        """
        url = reverse("authentication:username_available")
        data = {"username": "vera rubin"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.data,
            {
                "username": [
                    ErrorDetail(
                        string="Usernames can only contain alphanumeric characters, periods and underscores.",
                        code="invalid",
                    )
                ]
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
