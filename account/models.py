from django.db import models
from django.conf import settings
# Create your models here.
from django.urls import reverse

from django.conf import settings
from django.utils import timezone
from .fields import AvatarImageField

def manage_upload(instance, filename):
  print("[*] manage_upload  called")
  opts = {
    'user_id': instance.user.id,
    'file': filename,
    }
  return '{user_id}/{file}'.format(**opts)


class ProfileManager(models.Manager):
  def check_and_delete_avatar_image(self, profile):
    p = self.get(pk=profile.id)
    import os
    if p.img:
      os.remove(p.img.path)

class Profile(models.Model):
  class Meta:
    permissions = (
      ('can_change_profile', 'Can edit the profile'),
    )
  user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
  )

  img = AvatarImageField(
    default_width=200,
    default_height=200,
    upload_to=manage_upload,
    )
  description = models.TextField(max_length=200, default='', blank=True)
  actual_job = models.CharField(max_length=200, default='', blank=True)
  phone_number = models.CharField(max_length=100, default='', blank=True)
  num_contacts = models.PositiveIntegerField(default=0)

  objects = ProfileManager()
  def get_absolute_url(self):
    return reverse(
      'account:profile_detail',
      kwargs={
        'email': self.user.email
        }
      )

  def get_user_friends(self):
    return map(lambda x: x.to, self.contacts.all())

  def get_image(self):
    if not self.img:
      return '/static/svg/octoface.svg'
    else:
      return self.img.url
