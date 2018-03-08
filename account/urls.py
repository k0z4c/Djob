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
]

urlpatterns = [
    url(
        '^$',
        views.index,
        name='index',
        ),
    url(
        '^(?P<email>(\w)+@(\w)+\.(\w)+)/',
        include(some_urls),
        ),
]
