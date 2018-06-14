from django.dispatch import receiver
from marathon.signals import social_request_accepted
from marathon.models import SocialRequest
from .models import Skill

@receiver(social_request_accepted, sender=SocialRequest, weak=False)
def add_skill(sender, instance, **kwargs):
  if instance.label == 'skill_suggestion':
    Skill.objects.add(instance.to, instance.data.get('codename'))
