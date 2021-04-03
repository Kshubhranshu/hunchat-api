from django.test import TestCase

from authentication.models import User


class UserTests(TestCase):
    fixtures = ["users.json"]

    def test_is_username_taken(self):
        self.assertIs(User.is_username_taken("charles"), True)
        self.assertIs(User.is_username_taken("euclides"), False)

    def test_is_email_taken(self):
        self.assertIs(User.is_email_taken("marie@u-paris.fr"), True)
        self.assertIs(User.is_email_taken("rfranklin@cam.ac.uk"), False)
