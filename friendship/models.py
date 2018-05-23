from django.db import models
from django.conf import settings 
from account.models import Profile 
from django.apps import apps
from django.db.models import Q

class FriendshipManager(models.Manager):
  def get_friends_names_by_profile(self, profile):
    friendships = self.get_friendships_by_profile(profile)
    names = []
    for f in friendships:
      if f.by.user.email != profile.user.email:
        names.append(f.by.user.email)
      else:
        names.append(f.to.user.email)
    return names

  def get_friendships_by_profile(self, profile):
    qs = Q(to=profile) | Q(by=profile)
    return self.filter(qs)

# returns a qs list of users 
  # def get_friends(self, user):
  #   # list of friendships
  #   qs = Q(by=user.profile) | Q(to=user.profile)
  #   return self.filter(qs)

  def get_friends(self, user):
    qs = Q(profile__contacts_by__by=user.profile) | Q(profile__contacts_to__to=user.profile)
    # return apps.get_model(settings.AUTH_USER_MODEL).objects.filter(qs)

    # ?
    # friendships = self.get_friendships_by_profile(user.profile)
    # for f in friendships:
    #   qs += Q(by=f.by.user ) | Q(to=f.to)
    return apps.get_model(settings.AUTH_USER_MODEL).objects.filter(qs)


  def are_friends(self, profile1, profile2):
    self.get_friendships_by_profile(profile1)
    qs = self.get_friendships_by_profile(profile1).filter(Q(by=profile2) | Q(to=profile2)) 
    return qs.exists()

class Friendship(models.Model):
  by = models.ForeignKey(Profile, related_name='contacts_by')
  to = models.ForeignKey(Profile, related_name='contacts_to')

  date = models.DateTimeField(auto_now_add=True)
  objects = FriendshipManager()

  def save(self, *args, **kwargs):
    obj = super(Friendship, self).save(*args, **kwargs)
    # custom_post_save.send(
      
    #   )
    return obj 