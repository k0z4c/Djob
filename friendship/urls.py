from django.conf.urls import url
from . import views
urlpatterns = [
  url(
    r'^list/$',
    views.FriendshipListView.as_view(),
    name='list'
  ),
  url(
    r'^(?P<email>(\w)+@(\w)+\.(\w)+)/add',
    views.send_request,
    name='send_request'
  ),
  url(
    r'^pending/$',
    views.FriendshipRequestList.as_view(),
    name='friendship_list_pending'
  ),
]