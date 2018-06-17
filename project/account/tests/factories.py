import factory
import faker
from ..models import Profile
from django.db.models.signals import post_save

@factory.django.mute_signals(post_save)
class ProfileFactory(factory.DjangoModelFactory):
  class Meta:
    model = Profile

  user = factory.SubFactory('authentication.tests.factories.UserFactory', profile=None)
  actual_job = factory.Faker('job')
  description = factory.Faker('sentence')
