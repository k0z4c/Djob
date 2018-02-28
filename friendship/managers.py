from django.db import models
from .exceptions import FriendshipRequestExists
from django.db.models import Q

class FriendshipRequestManager(models.Manager):
    def send_request(self, by, to):
        request = self.filter(by=by, to=to)
        if request.exists():
            raise FriendshipRequestExists
        request = self.create(by=by, to=to)

class FriendshipManager(models.Manager):
    def are_friends(self, us1, us2):
        qs = self.filter(
            Q(by=us1) & Q(to=us2)
            |
            Q(by=us2) & Q(to=us1)
        )
        return qs.exists()

    def add_friend(self, us1, us2):
        if are_friends(us1, us2):
            raise FriendshipExists

        self.create(by=us1, to=us2)
        self.create(by=us2, to=us1)
