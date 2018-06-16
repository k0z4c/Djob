from django.test import TestCase
from .factories import UserFactory
from django.db import IntegrityError
# Create your tests here.

class UserTestCase(TestCase):

    def test_unique_email(self):
        u = UserFactory()
        with self.assertRaises(IntegrityError):
            UserFactory(email=u.email)
