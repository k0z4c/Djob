import random 

# no post_save, no permissions
def create_profiles(n):
  ProfileFactory.create_batch(n, user__password='password')

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

    fake = faker.Faker(providers=['faker.providers.lorem'])
    try:
      Skill.objects.bulk_create(
        Skill(profile=p, data=data, description=fake.sentence(nb_words=20)) for data in skills_data
      )
    except IntegrityError:
      pass


def create_friendships(min, max):
  for p in Profile.objects.all():
    friendship_to_create_no = random.choice(range(min, max))
    profiles = random.sample( set(Profile.objects.all().exclude(pk=p.pk)), friendship_to_create_no)
    try:
      Friendship.objects.bulk_create(
        ( Friendship(by=p, to=other) for other in profiles )
      )
      Friendship.objects.bulk_create(
        ( Friendship(by=other, to=p) for other in profiles )
      )
    except IntegrityError:
      pass

  for p in Profile.objects.all():
    p.num_contacts = p.contacts.count()
    p.save()


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
  import faker

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

  print("[*] Profiles created:")
  for p in Profile.objects.all():
    print('[*]', p)

  print("password: password")


