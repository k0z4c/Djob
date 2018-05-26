from django.dispatch import receiver
from marathon.signals import social_request_accepted
from .models import Friendship
from marathon.models import SocialRequest
from django.db import IntegrityError

@receiver(social_request_accepted, sender=SocialRequest)
def add_friend(sender, instance, **kwargs):
  if instance.label == 'friendship_request':
    try:
      Friendship.objects.create_friendship(
        by=instance.by, to=instance.to
        )
    except IntegrityError:
      pass
