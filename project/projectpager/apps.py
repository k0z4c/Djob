from django.apps import AppConfig


class ProjectpagerConfig(AppConfig):
    name = 'projectpager'

    def ready(self):
      from . import signals
