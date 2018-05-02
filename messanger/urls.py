from django.conf.urls import url
from . import views

urlpatterns = [
    # 'messages/create'
    url(
        r'^conversation/new/$',
        views.StartConversationView.as_view(),
        name='create_message'
    ),
    url(
        r'^conversation/(?P<pk>\d+)/reply/$',
        views.ConversationReplyView.as_view(),
        name='conversation_reply'
    ),
    url(
        r'^conversations/list/$',
        views.ConversationListView.as_view(),
        name='conversations'
    ),
    url(
        r'^conversations/(?P<pk>\d+)/messages/$',
        views.ConversationMessagesListView.as_view(),
        name='conversation_messages'
    ), 
    url(
        r'^ajax/conversations/unreaded_messages/$',
        views.unread_count,
        name='ajax_unreaded_count'
    ),
]