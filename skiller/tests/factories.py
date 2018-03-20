import factory
from ..models import Skill
from authentication.tests.factories import UserFactory

class SkillFactory(factory.DjangoModelFactory):
    class Meta:
        model = Skill

    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def user(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                user.skill_set.add(self)
