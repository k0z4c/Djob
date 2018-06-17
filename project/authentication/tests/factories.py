import factory
from django.test import TestCase
from ..models import User
from account.tests.factories import ProfileFactory
from account.models import Profile
from django.db.models.signals import post_save
import faker

@factory.django.mute_signals(post_save)
class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model=User

    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.Faker('password')
    profile = factory.RelatedFactory(ProfileFactory, 'user')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)
