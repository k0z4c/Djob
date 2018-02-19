from authentication.models import User
from friendship.models import Friendship
from friendship.models import FriendshipRequest
from account.models import Profile

us1 = User.objects.first()
us2 = User.objects.last()
