from django.test import TestCase
from account.tests.factories import ProfileFactory 
from django.db import IntegrityError
from ..exceptions import DuplicatedSkill
from ..models import Skill, SkillData 
from .factories import SkillFactory, SkillDataFactory
from django.test import Client
from django.core.urlresolvers import reverse 

from django.db.models import Q

class SkillModelTestCase(TestCase):
    def setUp(self):
        self.profile = ProfileFactory()
        self.data = SkillDataFactory(codename='testing')

    def test_user_add_skill_success(self):
        Skill.objects.create(profile=self.profile, data=self.data)
        self.assertTrue(Skill.objects.get(profile=self.profile, data=self.data))
        self.assertTrue(self.profile.skill_set.get(profile=self.profile, data=self.data))
        self.assertTrue(self.data.skill_set.get(profile=self.profile, data=self.data))

    def test_double_skill_error(self):
        Skill.objects.create(profile=self.profile, data=self.data)
        with self.assertRaises(IntegrityError):
            Skill.objects.create(profile=self.profile, data=self.data)

    def test_user_can_have_multiple_skills(self):
        data2 = SkillDataFactory(codename='test')

        Skill.objects.create(profile=self.profile, data=self.data)
        Skill.objects.create(profile=self.profile, data=data2)
        self.assertEqual(self.profile.skill_set.filter().count(), 2)

    def test_multiple_users_same_skill(self):
        p1 = ProfileFactory()
        p2 = ProfileFactory()

        Skill.objects.create(profile=p1, data=self.data)
        Skill.objects.create(profile=p2, data=self.data)

        skill_data = SkillData.objects.filter(_codename=self.data.codename)
        self.assertEqual(skill_data.count(), 1)

        # multiple refs
        skill_data = skill_data[0]
        self.assertEqual(skill_data.skill_set.count(), 2)

    def test_codename_is_decorated(self):
        sd = SkillDataFactory(codename='some skill')
        self.assertTrue(sd._codename, 'some_skill') 



    def tearDown(self):
        del self.profile
        del self.data



class SkillManagerTestCase(TestCase):
    def test_add_skill(self): 
        profile = ProfileFactory()

        skill_ass = Skill.objects.add(profile, name='testing')

        self.assertIsInstance(
            skill_ass, Skill,
            msg='The returned value must be an instance of Skill class'
            )
        self.assertTrue(
            SkillData.objects.get(_codename='testing') == skill_ass.data,
            msg='No SkillData instance allocated',
            )

        with self.assertRaises(DuplicatedSkill):
            Skill.objects.add(profile, name='testing')

    def test_user_can_have_multiple_skills(self):
        profile = ProfileFactory()
        Skill.objects.add(profile, name='testing')
        Skill.objects.add(profile, name='test')

        self.assertEqual(profile.skill_set.filter().count(), 2)

    def test_multiple_user_same_skill(self):
        profile1 = ProfileFactory()
        profile2 = ProfileFactory()

        Skill.objects.add(profile1, name='testing')
        Skill.objects.add(profile2, name='testing')

        self.assertEqual(
            Skill.objects.filter(
                Q(profile=profile1) | Q(profile=profile2)
                ).count(), 2
            )

        self.assertEqual(
            SkillData.objects.filter(_codename='testing').count(), 1
            )

class SkillAddViewTestCase(TestCase):
    # views tests
    def setUp(self):
        self.client = Client()
        self.profile = ProfileFactory(user__email='matt@gmail.com', user__password='pa55worD')
        self.client.login(email=self.profile.user.email, password='pa55worD')


    def test_get_add_skill(self):
        response = self.client.get(reverse('skill:add_skill'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response.context['form'],
            msg='no form in response') 


    def test_post_add_skill_redirect(self):
        response = self.client.post(
            reverse('skill:add_skill'),
            {'skill_name': 'pippo'},
            follow=True,
            )

        self.assertRedirects(
            response,
            reverse('account:profile_detail',
                args=((self.profile.user.email,)),
                )
            )

    def test_add_skill_success(self):
        codename = 'testing'
        response = self.client.post(
            reverse('skill:add_skill'),
            {' skill_name': codename, },
            follow=True
            )

        self.assertTrue(
            SkillData.objects.filter(_codename=codename).exists(),
        )

        from django.contrib.messages import SUCCESS
        queue = list(response.context['messages'])
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0].level, SUCCESS)



