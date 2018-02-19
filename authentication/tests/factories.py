import factory
from django.test import TestCase
from ..models import User

import faker

class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model=User
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
