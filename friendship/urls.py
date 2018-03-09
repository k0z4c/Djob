from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(
        # r'^(?P<email>(\w)+@(\w)+\.(\w)+)/$',
        r'^add_request/$',
        views.add_friendship_request,
        name='add_request'
    ),
    url(
        r'^index/$',
        views.IndexView.as_view(),
        name='index'
    ),
    url(
        r'^show_friendships/$',
        views.FriendshipListView.as_view(),
        name='show_friendships'
    ),
    url(
        r'^req_received/$',
        views.FriendshipRequestReceivedListView.as_view(),
        name='requests_received'
    ),
    url(
        r'^req_sent/$',
        views.FriendshipRequestSentListView.as_view(),
        name='requests_sent'
    ),
    url(
        r'^ajax/remove_friendship/$',
        views.remove_friendship,
        name='remove_friendship',
    ),
    url(
        r'^ajax/unread_friendship/$',
        views.friendship_notifications_count,
        name='friendship_notifications_count'
    ),
    url(
        r'^(?P<pk>[0-9]+)/accept/$',
        views.accept_request,
        name='request_accept',
    ),
    # url(
    #     r'^(?P<pk>[0-9]+)/reject/$',
    #     views.reject_request,
    #     name='request_reject'
    # ),

]
