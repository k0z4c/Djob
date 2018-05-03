from django.conf.urls import url
from . import views
urlpatterns = [
  url(
    r'^ajax/inbox/count$',
    views.unread_count,
    name='ajax_unread_counter',
    ),
]