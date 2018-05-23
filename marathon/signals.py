import django.dispatch

# providing_args: declares parameters passed to receiver func; e.g. instance 
social_request_accepted = django.dispatch.Signal(providing_args=['instance',])
social_request_rejected = django.dispatch.Signal(providing_args=['instance',])

from django.dispatch import receiver
from django.db.models.signals import post_save 
from notifications.signals import notify

@receiver(post_save, sender='marathon.SocialRequest')
def generate_notification(sender, created, instance,  **kwargs):
  if not created: 
    return
  notify.send(
    instance.by,
    recipient=instance.to,
    verb='request',
    description=instance.tile,
    target=instance
    )