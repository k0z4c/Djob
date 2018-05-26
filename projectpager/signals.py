from django.dispatch import receiver
from marathon.models import SocialRequest
from marathon.signals import social_request_accepted

@receiver(social_request_accepted, sender=SocialRequest)
def add_member_to_page(sender, instance, **kwargs):
  if instance.label == 'invite_request':
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    from .models import ProjectPage

    content_type = ContentType.objects.get_for_model(ProjectPage)
    permission = Permission.objects.get(
      content_type=content_type,
      codename='can_post_discussions'
      )
    instance.to.user.user_permissions.add(permission)
