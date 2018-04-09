from django.test import TestCase

from authentication.tests.factories import UserFactory 
from django.db import IntegrityError
from ..exceptions import DuplicatedSkill
from ..models import Skill, SkillData 
from .factories import SkillFactory 
from django.test import Client
from django.core.urlresolvers import reverse 


class SkillModelTestCase(TestCase):
    # models integrity checks 
    def test_double_skill_association_fail(self):
        skill = SkillFactory(data__codename='hey')
        with self.assertRaises(IntegrityError):
            SkillFactory(user=skill.user, data___codename='hey')

    def test_manager_add_skill(self):
        skill_association = Skill.objects.add_skill(user=UserFactory(), name='hey man')

        # add skill that not exists 
        skill_data = SkillData.objects.get(_codename='hey_man')
        self.assertEqual(skill_data._codename, 'hey_man')

        with self.assertRaises(DuplicatedSkill):
            Skill.objects.add_skill(user=skill_association.user, name='hey man')


class SkillViewTestCase(TestCase):
    # views tests
    def setUp(self):
        self.client = Client()
        self.user = UserFactory(email='matt@gmail.com', password='pa55worD')
        self.client.login(username=self.user.email, password='pa55worD')


    def test_get_create_skill(self):
        response = self.client.get(reverse('skill:add_skill'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form']) 


    def test_post_add_skill_redirect(self):
        response = self.client.post(
            reverse('skill:add_skill'),
            {'_codename': 'pippo'},
            follow=True,
            )

        self.assertRedirects(
            response,
            reverse('account:profile_detail',
                args=((self.user.email,)),
                )
            )

    def test_post_add_skil_message_success(self):
        response = self.client.post(
            reverse('skill:add_skill'),
            {'_codename': 'skill'},
            follow=True,
            )

        from django.contrib.messages import SUCCESS
        queue = list(response.context['messages'])
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0].level, SUCCESS)

    def test_post_add_skill_message_error_double_skill(self):
        response = self.client.post(
                reverse('skill:add_skill'),
                {'_codename': 'skill'},
                follow=True,
                )

        response = self.client.post(
                reverse('skill:add_skill'),
                {'_codename': 'skill'},
                follow=True,
                )

        from django.contrib.messages import ERROR
        queue = list(response.context['messages']) 
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0].level, ERROR)       
