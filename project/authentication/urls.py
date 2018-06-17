from .import views
from django.conf.urls import(
    url, include
)

urlpatterns = [
    url(
        r'^signup/$',
        views.SignupView.as_view(),
        name='signup'
    ),
    url(
        r'^login/$',
        views.CustomLoginView.as_view(),
        name='login'
    ),
    url(
        r'^thanks/$',
        views.ThanksView.as_view(),
        name='thanks'
    ),
    url(
        r'^',
        include(
            'django.contrib.auth.urls'
        )
    ),
]
