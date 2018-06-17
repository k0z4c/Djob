from django.conf.urls import url, include
from . import views

some_urls = [
    url(
        '^$',
        views.ProfileDetailView.as_view(),
        name='profile_detail'
        ),
    url(
        '^edit/$',
        views.EditAccountView.as_view(),
        name='profile_edit'
        ),
    url(
        '^notifications/unread/$',
        views.UnreadedNotificationsListView.as_view(),
        name='notifications_unread'
        ),
    url(
        '^notifications/read/$',
        views.ReadedNotificationsListView.as_view(),
        name='notifications_read'
        )
]

urlpatterns = [
    url(
        '^$',
        views.index,
        name='index',
        ),
    url(
        r'^(?P<email>([\w\.\+\-])+@([\w\.\+\-])+(\w)+)/',
        include(some_urls),
        ),
]
