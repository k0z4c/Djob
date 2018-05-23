from django.apps import AppConfig


class SkillerConfig(AppConfig):
    name = 'skiller'

    def ready(self):
      import skiller.signals

