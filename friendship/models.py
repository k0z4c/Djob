from django.db import models
from django.conf import settings 

from django.db.models import Q

class FriendshipManager(models.Manager):
  def get_friends(self, user):
    qs = Q(to=user) | Q(by=user)
    return self.filter(qs)

  def are_friends(self, us1, us2):
    self.get_friends(us1)
    qs = self.get_friends(us1).filter(Q(by=us2) | Q(to=us2)) 
    return qs.exists()

class Friendship(models.Model):
  by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
  to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')

  date = models.DateTimeField(auto_now_add=True)
  objects = FriendshipManager()

  def save(self, *args, **kwargs):
    obj = super(Friendship, self).save(*args, **kwargs)
    # custom_post_save.send(
      
    #   )
    return obj 