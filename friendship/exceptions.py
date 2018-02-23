from django.db import IntegrityError

class FriendshipRequestExists(IntegrityError):
    pass

class FriendshipExists(IntegrityError):
    pass
