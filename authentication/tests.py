from django.test import TestCase

from rest_framework.test import APITestCase, URLPatternsTestCase

from authentication.models import User


class UserModelTests(TestCase):
    # fixtures = ["users.json"]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            name="Charles Darwin", username="charles", email="charles@hmsbeagle.com"
        )

    def test_is_username_taken(self):
        self.assertIs(User.is_username_taken("charles"), True)
        self.assertIs(User.is_username_taken("marie"), False)
