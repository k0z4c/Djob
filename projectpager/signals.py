from django.dispatch import receiver
from marathon.models import SocialRequest
from django.db.models.signals import post_save
from marathon.signals import social_request_accepted
from django.core import serializers
from .models import ProjectPage
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

@receiver(social_request_accepted, sender=SocialRequest)
def add_member_to_page(sender, instance, **kwargs):
  if instance.label == 'invite_request':
    content_type = ContentType.objects.get_for_model(ProjectPage)
    permission = Permission.objects.get(
      content_type=content_type,
      codename='can_post_discussions'
      )
    projectpage = list(
      serializers.deserialize('json', instance.data['project'])
    )[0].object
    projectpage.refresh_from_db()
    projectpage.profiles.add(instance.to)
    instance.to.user.user_permissions.add(permission)

@receiver(post_save, sender=ProjectPage)
def add_owner_to_profiles(sender, instance, created, **kwargs):
  if created:
    owner = instance.owner
    instance.profiles.add(owner)
