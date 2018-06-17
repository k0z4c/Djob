import random 

# no post_save, no permissions
def create_profiles(n):
  return ProfileFactory.create_batch(n, user__password='password')

def load_skill_data(verbose=False):
  with open('skills.data', 'rb') as f:
    skill_list = pickle.loads(f.read())

  for skill_name in (s for s in skill_list):
    if verbose: print(skill_name)
    try:
      SkillData.objects.create(codename=skill_name)
    except IntegrityError:
      pass

def assign_skills(min, max):
  for p in Profile.objects.all():
    skill_to_assign_number = random.choice(range(min, max))
    skills_data = random.sample( set(SkillData.objects.all()), skill_to_assign_number)

    try:
      Skill.objects.bulk_create(
        Skill(profile=p, data=data) for data in skills_data
      )
    except IntegrityError:
      pass


def create_friendships(min, max):
  for p in Profile.objects.all():
    friendship_to_create_no = random.choice(range(min, max))
    profiles = random.sample( set(Profile.objects.all()), friendship_to_create_no)
    print('profiles selected', profiles)
    try:
      Friendship.objects.bulk_create(
        ( Friendship(by=p, to=other) for other in profiles )
      )
    except IntegrityError:
      pass


if __name__ == '__main__':
  import os
  import django

  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djob.settings')
  django.setup()

  from authentication.tests.factories import ProfileFactory
  from skiller.models import SkillData, Skill
  from account.models import Profile
  from friendship.models import Friendship


  from django.db import IntegrityError
  import pickle

  print("[*] creating profiles..")
  create_profiles(20)
  print("[*] loading skill data...")
  load_skill_data(verbose=False)
  print("[*] assigning skills...")
  # min, max skills to assign to each profile
  assign_skills(3, 7)
  print("[*] create friendships...")
  create_friendships(4, 7)
  print("[*] ...done")


