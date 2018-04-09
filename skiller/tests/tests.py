from django.test import TestCase

from authentication.tests.factories import UserFactory 
from django.db import IntegrityError
from ..exceptions import DuplicatedSkill
from ..models import Skill, SkillData 
from .factories import SkillFactory, SkillDataFactory
from django.test import Client
from django.core.urlresolvers import reverse 


class SkillModelTestCase(TestCase):
    def test_user_add_skill_success(self):
        user = UserFactory()
        data = SkillDataFactory(codename='testing')

        Skill.objects.create(user=user, data=data)
        self.assertTrue(Skill.objects.get(user=user, data=data))
        self.assertTrue(user.skill_set.get(user=user, data=data))
        self.assertTrue(data.skill_set.get(user=user, data=data))


class SkillManagerTestCase(TestCase):
    def test_add_skill(self): 
        user = UserFactory()

        skill_ass = Skill.objects.add(user, name='testing')

        self.assertIsInstance(
            skill_ass, Skill,
            msg='The returned value must be an instance of Skill class'
            )
        self.assertTrue(
            SkillData.objects.get(_codename='testing') == skill_ass.data,
            msg='No SkillData instance allocated',
            )

        with self.assertRaises(DuplicatedSkill):
            Skill.objects.add(user, name='testing')


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

       
