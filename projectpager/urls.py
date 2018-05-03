from django.conf.urls import url
from . import views

urlpatterns = [
  url(
    r'^new/$',
    views.ProjectPageCreateView.as_view(),
    name='projectpage_create'
  ),
]