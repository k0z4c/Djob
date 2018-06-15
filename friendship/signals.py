from django.dispatch import receiver
from marathon.signals import social_request_accepted
from .models import Friendship
from marathon.models import SocialRequest
from django.db import IntegrityError
from django.db.models.signals import post_delete
from notifications.signals import notify

@receiver(social_request_accepted, sender=SocialRequest)
def add_friend(sender, instance, **kwargs):
  if instance.label == 'friendship_request':
    try:
      Friendship.objects.create_friendship(
        by=instance.by, to=instance.to
        )
    except IntegrityError:
      pass
    notify.send(
      sender=instance.to.user,
      recipient=instance.by.user,
      verb='friendship_is_accepted_by',
      description='{} has accepted you friendship request!'.format(instance.to.user)
    )

@receiver(post_delete, sender=Friendship)
def remove_friendship(sender, instance, using, **kwargs):
  Friendship.objects.filter(by=instance.to, to=instance.by).delete()
