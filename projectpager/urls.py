from django.conf.urls import url, include
from . import views

project_urls = [
  url(
    r'^projects/create/$',
    views.ProjectPageCreateView.as_view(),
    name='project_create'
  ),
  url(
    r'^projects/list/$',
    views.ProjectPageListView.as_view(),
    name='list_projects'
  ),
  url(
    r'^projects/(?P<project_pk>\d+)/detail/$',
    views.ProjectPageDetailView.as_view(),
    name='project_detail'
  ),
  url(
    r'^projects/invite/$',
    views.InviteRequestFormView.as_view(),
    name='invite'
  ),
  url(
    r'^projects/(?P<project_pk>\w+)/update/$',
    views.ProjectPageUpdateView.as_view(),
    name='project_update',
  ),
  url(
    r'^projects/(?P<project_pk>\w+)/thread/create/$',
    views.ThreadCreateView.as_view(),
    name='create_thread',
  ),
  url(
    r'projects/(?P<project_pk>\w+)/thread/(?P<thread_pk>\w+)/post/$',
    views.MessageCreateView.as_view(),
    name='thread_create_message',
  ),
  url(
    r'^projects/(?P<project_pk>\w+)/thread/(?P<thread_pk>\w+)/detail/$',
    views.ThreadDetailView.as_view(),
    name='thread_detail',
  ),
]

urlpatterns = [
  url(
      r'^(?P<email>(\w)+@(\w)+\.(\w)+)/',
      include(project_urls),
  ),
]

