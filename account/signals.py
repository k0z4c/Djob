from django.dispatch import receiver
from django.db.models.signals import post_save

from django.conf import settings
from django.apps import apps

from .models import Profile

USER_MODEL = settings.AUTH_USER_MODEL

@receiver(post_save, sender=apps.get_model(USER_MODEL))
def create_profile(sender, **kwargs):
    if kwargs.get('created'):
        Profile.objects.create(
        user=kwargs.get('instance')
    )
