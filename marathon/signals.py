from django.dispatch import receiver
from notifications.signals import notify
from django.db.models.signals import post_save 
from django.db.models.signals import ModelSignal

social_request_accepted = ModelSignal(providing_args=['instance',])
social_request_rejected = ModelSignal(providing_args=['instance',])


@receiver(post_save, sender='marathon.SocialRequest')
def generate_notification(sender, created, instance,  **kwargs):
  if created: 
    notify.send(
      instance.by.user,
      recipient=instance.to.user,
      verb='request',
      description=instance.tile,
      target=instance
      )

@receiver(social_request_rejected, sender='marathon.SocialRequest')
@receiver(social_request_accepted, sender='marathon.SocialRequest')
def mark_disabled(sender, instance, **kwargs):
  same_type_requests = instance.__class__.objects.filter(
    label=instance.label,
    status=instance.__class__.PENDING,
    to=instance.to,
    data=instance.data,
  ).exclude(pk=instance.pk)

  same_type_requests.update(
    status=instance.__class__.DISABLED
  )
