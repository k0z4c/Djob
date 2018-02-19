import factory
from ..models import FriendshipRequest, Friendship
from authentication.tests.factories import UserFactory

class FriendshipRequestFactory(factory.DjangoModelFactory):
    class Meta:
        model = FriendshipRequest
    by = factory.SubFactory(UserFactory)
    to = factory.SubFactory(UserFactory)

class FriendshipFactory(factory.DjangoModelFactory):
    class Meta:
        model = Friendship
    by = factory.SubFactory(UserFactory)
    to = factory.SubFactory(UserFactory)
    
