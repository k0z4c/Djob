from django.dispatch import receiver
from marathon.signals import social_request_accepted
from .models import Friendship
from marathon.models import SocialRequest
from django.db import IntegrityError

@receiver(social_request_accepted, sender=SocialRequest, weak=False)
def add_friend(sender, instance, **kwargs):
  print('signal received')
  print(instance.label)
  if instance.label == 'friendship_request':
    try:
      Friendship.objects.create(by=instance.by, to=instance.to)
    except IntegrityError:
      pass
