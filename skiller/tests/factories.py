import factory
from ..models import Skill
from authentication.tests.factories import UserFactory

class SkillFactory(factory.DjangoModelFactory):
    class Meta:
        model = Skill

    user = factory.SubFactory(UserFactory)
