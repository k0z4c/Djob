from authentication.models import User
from friendship.models import Friendship
from account.models import Profile
from notifications.models import Notification
from marathon.models import SocialRequest
from skiller.models import Skill, SkillData
import random

def del_all_notifications():
  for l in Notification.objects.all(): l.delete()
  for l in SocialRequest.objects.all(): l.delete()

# us1 = User.objects.first()
# us2 = User.objects.last()

def create_users():
  mails = ['matt', 'antonio', 'giulia', 'fabio', 'luca', 'enri' ,'manu', 'vinnie' ]
  password = 'somepa55w0rd'
  for m in mails:
    User.objects.create_user(email=m+'@gmail.com', password=password)

def create_skills():
  names = ['c++', 'hr', 'coding', 'architect', 'excel', 'pentester']
# from recommander.engine import PredictionEngine
# engine = PredictionEngine(us1.profile, Profile.objects.all(), [('contacts', 'to'), ('skill_set', 'data'), 'projectpages'])
# engine.predict()
  for n in names:
    SkillData.objects.create(_codename=n)

def create_friendships():
  for i in range(1,10):
    first = random.choice(Profile.objects.all())
    second = random.choice(Profile.objects.all())
    if not Friendship.objects.are_friends(first, second):
      Friendship.objects.create_friendship(by=first, to=second)

def create_skill_user():
  for i in range(1,10):
    profile = random.choice(Profile.objects.all())
    skilldata = random.choice(SkillData.objects.all())
    try:
      Skill.objects.add(profile, skilldata.codename)
    except Exception: pass

def get_profile(name):
  return Profile.objects.filter(user__email__startswith=name).get()

def print_users(model, attr):
  for i in model.objects.all():
    if isinstance(attr, tuple):
      print(getattr(getattr(i, attr[0]), attr[1]))
    else:
      print(getattr(i, attr))

def get_profile_request_recv_data(profile):
  for r in profile.marathon_received.all():
    if getattr(r, 'data'): print(r.data)
