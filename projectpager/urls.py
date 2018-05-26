from django.conf.urls import url
from . import views

urlpatterns = [
  url(
    r'^projects/create/$',
    views.ProjectPageCreateView.as_view(),
    name='projectpage_create'
  ),
  url(
    r'^projects/list/$',
    views.ProjectPageListView.as_view(),
    name='projectpage_list'
  ),
  url(
    r'projects/^(?P<pk>\w+)/detail/$',
    views.ProjectPageDetailView.as_view(),
    name='project_page_detail'
  ),
  url(
    r'projects/invite/$',
    views.InviteRequestFormView.as_view(),
    name='project_page_invite'
  ),
  url(
    r'^projects/(?P<pk>\w+)/update/$',
    views.ProjectPageUpdateView.as_view(),
    name='project_page_update',
  )
]