from .models import ProjectPage
from django.core import serializers
from django.dispatch import receiver
from marathon.models import SocialRequest
from marathon.signals import social_request_accepted
from guardian.shortcuts import assign_perm
from django.db.models.signals import post_save

@receiver(social_request_accepted, sender=SocialRequest)
def add_member_to_page(sender, instance, **kwargs):
  if instance.label == 'invite_request':
    projectpage = list(
      serializers.deserialize('json', instance.data['project'])
    )[0].object

    projectpage.refresh_from_db()
    projectpage.profiles.add(instance.to)
    assign_perm('can_open_threads', instance.to.user, projectpage)

@receiver(post_save, sender=ProjectPage)
def add_owner_to_profiles(sender, instance, created, **kwargs):
  if created:
    owner = instance.owner
    instance.profiles.add(owner)
    assign_perm('can_open_threads', instance.owner.user, instance)
