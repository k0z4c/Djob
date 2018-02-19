from django.apps import AppConfig

from django.dispatch import receiver
from django.db.models.signals import post_save

class AccountConfig(AppConfig):
    name = 'account'

    def ready(self):
        from . import signals
