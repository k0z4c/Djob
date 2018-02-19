from django.conf.urls import url, include
from .import views

urlpatterns = [
    url(
        r'^signup/$',
        views.signup,
        name='signup'
    ),
    url(
        r'^checkpoint/$',
        views.checkpoint,
        name='checkpoint'
    ),
    url(
        r'^login/$',
        views.CustomLoginView.as_view(),
        name='login'
    ),
    url(
        r'^',
        include(
            'django.contrib.auth.urls'
        )
    ),
]
