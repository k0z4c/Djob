from django.dispatch import receiver
from marathon.signals import social_request_accepted
from .models import Friendship
from marathon.models import SocialRequest
from django.db import IntegrityError

@receiver(social_request_accepted, sender=SocialRequest)
def add_friend(sender, instance, **kwargs):
  print('signal received')
  try:
    Friendship.objects.create(by=instance.by, to=instance.to)
  except IntegrityError:
    pass

from django.db.models.signals import post_save
@receiver(post_save, sender=SocialRequest)
def testing(sender, **kwargs):
  print("testing")
