from django.conf.urls import url
from . import views

urlpatterns = [
  url(
    r'^ajax/(?P<pk>\d+)/request/$',
    views.manage_request,
    name='manage_request'
  ),
]
