from authentication.models import User
from friendship.models import Friendship
from account.models import Profile
from notifications.models import Notification
from marathon.models import SocialRequest

def del_all_notifications():
  for l in Notification.objects.all(): l.delete()
  for l in SocialRequest.objects.all(): l.delete()

us1 = User.objects.first()
us2 = User.objects.last()
