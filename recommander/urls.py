from django.conf.urls import url, include
from . import views

urlpatterns = [
  url(
      r'^(?P<email>(\w)+@(\w)+\.(\w)+)/',
      views.SuggestView.as_view(),
      name='suggest'
      ),
]