from django.db import models
from .exceptions import FriendshipRequestExists
from django.db.models import Q

from authentication.models import User 

class FriendshipRequestManager(models.Manager):
    def send_request(self, by, to):
        request = self.filter(by=by, to=to)
        if request.exists():
            raise FriendshipRequestExists
        request = self.create(by=by, to=to)

    def check_request(self, by, to):
        q = Q(by=by, to=to) | Q(by=to, to=by)
        return self.filter(q).exists()

class FriendshipManager(models.Manager):
    def get_friends(self, user):
        '''returns a queryset of User friends'''
        qs = User.objects.filter(
            contacts__to=user,
            )
        return qs 

    def are_friends(self, us1, us2):
        qs = self.filter(
            Q(by=us1) & Q(to=us2)
            |
            Q(by=us2) & Q(to=us1)
        )
        return qs.exists()

    def add_friend(self, us1, us2):
        if self.are_friends(us1, us2):
            raise FriendshipExists

        self.create(by=us1, to=us2)
        self.create(by=us2, to=us1)

    def remove_friendship(self, us1_id, us2_id):
        qs = Q(by=us1_id, to=us2_id) | Q(by=us2_id, to=us1_id)
        tpl = self.filter(qs)
        print('removing ')
        print(tpl)
        for i in tpl:
            i.delete()
