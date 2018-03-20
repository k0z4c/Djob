from django.test import TestCase

# Create your tests here.

# TODO: some tests on model 
from .factories import SkillFactory
from ..models import Skill, Confirmation
from ..exceptions import SkillExists
from authentication.tests.factories import UserFactory 

from django.db import IntegrityError
class SkillTestCase(TestCase):
    # manager tests
    def test_decorate_name(self):
        bad_codename = "sk i    "
        user = UserFactory()

        skill = Skill.manager.create_skill(user=user, name=bad_codename)
        self.assertEqual(skill.codename, 'sk_i')

    def test_skill_exists_error(self):
        user = UserFactory()
        codename = 'this is a codename'

        Skill.manager.create_skill(user=user, name=codename) 
        with self.assertRaises(SkillExists):
            Skill.manager.create_skill(user=user, name=codename)

    # integrity tests 
    def test_same_user_double_confirmation_error(self):
        user = UserFactory()
        user_confirming = UserFactory()

        skill = SkillFactory(codename='ski', user=(user,))
        confirm = Confirmation.objects.create(to=user, by=user_confirming, skill=skill)
        with self.assertRaises(IntegrityError):
            Confirmation.objects.create(to=user, by=user_confirming, skill=skill)

    def test_double_codename_skill(self):
        skill = SkillFactory(codename='coder')
        with self.assertRaises(IntegrityError):
            SkillFactory(codename='coder')


