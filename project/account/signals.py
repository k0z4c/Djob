from django.dispatch import receiver
from django.db.models.signals import post_save

from django.conf import settings
from django.apps import apps

from guardian.shortcuts import assign_perm
from .models import Profile

from friendship.models import Friendship
from django.db.models import F

USER_MODEL = settings.AUTH_USER_MODEL

# qua perche non mettere user passes test quando accede alla view di modifica?
@receiver(post_save, sender=apps.get_model(USER_MODEL))
def create_profile(sender, **kwargs):
    if kwargs.get('created'):
        profile = Profile.objects.create(
            user=kwargs.get('instance')
        )
        assign_perm('can_change_profile', kwargs.get('instance'), profile)

@receiver(post_save, sender=Friendship, dispatch_uid='increment')
def increment_num_contacts(sender, instance, created, **kwargs):
  print(created)
  if created:
    instance.by.num_contacts = F('num_contacts') + 1
    # instance.to.num_contacts=F('num_contacts') + 1
    instance.by.save()
