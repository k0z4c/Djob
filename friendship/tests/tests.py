from django.test import TestCase
from .factories import FriendshipRequestFactory, FriendshipFactory
from ..models import FriendshipRequest, Friendship
from authentication.tests.factories import UserFactory
from django.db import IntegrityError

from ..exceptions import FriendshipExists
# Create your tests here.

class FriendshipManagerTestCase(TestCase):
    def test_is_friend_true(self):
        friendship = FriendshipFactory()
        us1 = friendship.by
        us2 = friendship.to

        self.assertEqual(Friendship.objects.is_friend(us1, us2), True)

    def test_is_friend_false(self):
        us1 = UserFactory()
        us2 = UserFactory()

        self.assertEqual(Friendship.objects.is_friend(us1, us2), False)


class FriendshipRequestManagerTestCase(TestCase):

    def setUp(self):
        self.us1 = UserFactory()
        self.us2 = UserFactory()

    def test_send_request_returns(self):
        '''us1 send a request to us2'''
        request = FriendshipRequest.objects.send_request(by=self.us1, to=self.us2)
        db_request = FriendshipRequest.objects.first()
        '''returns the request'''
        # self.assertEqual(request, db_request)

        '''double request returns None'''
        with self.assertRaises(FriendshipExists):
            FriendshipRequest.objects.send_request(by=self.us1, to=self.us2)

    def tearDown(self):
        del self.us1
        del self.us2

class FriendshipRequestTestCase(TestCase):
    def test_two_friendhship_error(self):
        us1 = UserFactory()
        us2 = UserFactory()

        FriendshipRequest.objects.create(by=us1, to=us2)
        with self.assertRaises(IntegrityError):
            FriendshipRequest.objects.create(by=us1, to=us2)

class FriendshipTestCase(TestCase):
    def setUp(self):
        self.us1 = UserFactory()
        self.us2 = UserFactory()

    def test_two_friendship_by_error(self):
        Friendship.objects.create(by=self.us1, to=self.us2)
        with self.assertRaises(IntegrityError):
            Friendship.objects.create(by=self.us1, to=self.us2)

    def test_two_friendship_to_error(self):
        pass
