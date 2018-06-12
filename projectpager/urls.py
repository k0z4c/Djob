from django.conf.urls import url, include
from . import views

some_urls = [
  url(
    r'^projects/create/$',
    views.ProjectPageCreateView.as_view(),
    name='create'
  ),
  url(
    r'^projects/list/$',
    views.ProjectPageListView.as_view(),
    name='list'
  ),
  url(
    r'^projects/(?P<pk>\d+)/detail/$',
    views.ProjectPageDetailView.as_view(),
    name='detail'
  ),
  url(
    r'^projects/invite/$',
    views.InviteRequestFormView.as_view(),
    name='invite'
  ),
  url(
    r'^projects/(?P<pk>\w+)/update/$',
    views.ProjectPageUpdateView.as_view(),
    name='update',
  ),
  url(
    r'^projects/(?P<pk>\w+)/thread/create/$',
    views.ThreadCreateView.as_view(),
    name='create_thread',
  ),
  url(
    r'^projects/(?P<pk>\w+)/thread/(?P<thread_pk>\w+)/post/$',
    views.MessageCreateView.as_view(),
    name='thread_create_message',
  ),
  url(
    r'^projects/(?P<pk>\w+)/thread/(?P<thread_pk>\w+)/detail/$',
    views.ThreadDetailView.as_view(),
    name='thread_detail',
  ),
] 
urlpatterns = [
  url(
      r'^(?P<email>(\w)+@(\w)+\.(\w)+)/',
      include(some_urls),
  ),
]