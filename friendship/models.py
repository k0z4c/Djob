from django.db import models

from django.conf import settings
from django.utils import timezone

from . import managers
# Create your models here.

class FriendshipRequest(models.Model):
    by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requests_sent')
    to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requests_received')

    read = models.BooleanField(default=False)
    objects = managers.FriendshipRequestManager()
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [('by', 'to')]

    def accept(self):
        Friendship.objects.create(by=self.by, to=self.to)
        Friendship.objects.create(by=self.to, to=self.by)

        self.delete()

class Friendship(models.Model):

    by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contacts')
    to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')

    date = models.DateTimeField(default=timezone.now)

    objects = managers.FriendshipManager()
    class Meta:
        unique_together = [('by', 'to'), ('to', 'by')]
    def __str__(self):
        return self.to.email
