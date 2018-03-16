from django.test import TestCase

# Create your tests here.

# TODO: some tests on model 
from .factories import SkillFactory
from ..models import Skill 
from ..exceptions import SkillExists
from authentication.tests.factories import UserFactory 

from django.db import IntegrityError
class SkillTestCase(TestCase):

    def test_decorate_name(self):
        bad_codename = "sk i    "
        user = UserFactory()

        skill = Skill.manager.insert_skill(user=user, name=bad_codename)
        self.assertEqual(skill.codename, 'sk_i')

    def test_skill_exists_error(self):
        user = UserFactory()
        codename = 'this is a codename'

        Skill.manager.insert_skill(user=user, name=codename) 
        with self.assertRaises(SkillExists):
            Skill.manager.insert_skill(user=user, name=codename)

