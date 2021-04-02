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


class EmailAvailableViewTests(APITestCase, URLPatternsTestCase):
    fixtures = ["users.json"]
    urlpatterns = [
        path("api/", include("authentication.urls")),
    ]

    def test_email_is_available(self):
        """
        Ensure we get a message indicating that an email is available for an available email.
        """
        url = reverse("authentication:email_available")
        data = {"email": "jocelynbellturner@ucl.ac.uk"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.data, {"email": "Email available."})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_email_is_not_available(self):
        """
        Ensure we get a message indicating that an email is NOT available for an email already in use.
        """
        url = reverse("authentication:email_available")
        data = {"email": "marie@u-paris.fr"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.data,
            {
                "email": [
                    ErrorDetail(
                        string="An account for the email already exists.",
                        code="invalid",
                    )
                ]
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_is_not_valid(self):
        """
        Ensure we get a message indicating that an email has invalid format for an email with invalid format.
        """
        url = reverse("authentication:email_available")
        data = {"email": "verarubin@"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.data,
            {
                "email": [
                    ErrorDetail(string="Enter a valid email address.", code="invalid")
                ]
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
