import factory
from ..models import Skill, SkillData
from authentication.tests.factories import UserFactory

class SkillDataFactory(factory.DjangoModelFactory):
    class Meta:
        model = SkillData

    codename = factory.Faker('first_name')
        
class SkillFactory(factory.DjangoModelFactory):
    class Meta:
        model = Skill

    user = factory.SubFactory(UserFactory)
    data = factory.SubFactory(SkillDataFactory)

    # @factory.post_generation
    # def user(self, create, extracted, **kwargs):
    #     if not create:
    #         return

    #     if extracted:
    #         for user in extracted:
    #             user.skill_set.add(self)
