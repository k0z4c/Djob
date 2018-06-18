from django.db import models
from django.conf import settings
from django.urls import reverse
from django.conf import settings
from .fields import AvatarImageField
from django.contrib.contenttypes.fields import GenericRelation

def manage_upload(instance, filename):
  opts = {
    'user_id': instance.user.id,
    'file': filename,
    }
  return '{user_id}/{file}'.format(**opts)

class Profile(models.Model):
  user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
  )

  activities = GenericRelation('recommander.Activity')

  description = models.TextField(max_length=400, default='', blank=True)
  actual_job = models.CharField(max_length=200, default='', blank=True)
  num_contacts = models.PositiveIntegerField(default=0)
  img = AvatarImageField(
    default_width=200,
    default_height=200,
    upload_to=manage_upload,
    blank=True
    )

  def get_absolute_url(self):
    return reverse(
      'account:profile_detail',
      kwargs={
        'email': self.user.email
        }
      )

  def is_friend(self, profile):
    return profile.contacts.filter(to=self).exists()

  def get_user_friends(self):
    return map(lambda x: x.to, self.contacts.all())

  def get_image(self):
    if not self.img:
      return '/media/default.svg'
    else:
      return self.img.url

  def __str__(self):
    return self.user.email

