from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(
        # r'^(?P<email>(\w)+@(\w)+\.(\w)+)/$',
        r'^add_request/$',
        views.add_friendship_request,
        name='add_request'
    ),
]
