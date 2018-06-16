from django.conf.urls import url
from . import views
urlpatterns = [
  url(
    r'^(?P<email>([\w\.\+\-])+@(\w)+\.(\w)+)/list/$',
    views.FriendshipListView.as_view(),
    name='list'
  ),
  url(
    r'^(?P<email>([\w\.\+\-])+@(\w)+\.(\w)+)/network/$',
    views.NetworkList.as_view(),
    name='network'
  ),
  url(
    r'^(?P<email>([\w\.\+\-])+@(\w)+\.(\w)+)/add',
    views.send_request,
    name='send_request'
  ),
  # eliminare
  url(
    r'^pending/$',
    views.FriendshipRequestList.as_view(),
    name='friendship_list_pending'
  ),
]