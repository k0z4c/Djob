from django.conf.urls import url
from . import views

urlpatterns = [
    # 'messages/create'
    url(
        r'^messages/new/$',
        views.CreateMessageView.as_view(),
        name='create_message'
    ),
    url(
        r'^conversations/list/',
        views.ConversationListView.as_view(),
        name='conversations'
    ),
    url(
        r'^conversations/(?P<pk>\d+)/messages/',
        views.ConversationDetailView.as_view(),
        name='conversation_messages'
    ), 
]