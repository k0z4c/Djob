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
        'datetime': timezone.now(),
        'file': filename,
        }
    return '{user_id}/{datetime:%Y/%m/%d}/{file}'.format(**opts)


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
    description = models.TextField(max_length=200)
    actual_job = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse(
            'account:profile_detail',
            kwargs={
                'email': self.user.email
                }
            )
