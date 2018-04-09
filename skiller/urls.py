from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^add/$',
        views.SkillAddView.as_view(),
        name='add_skill',
    ),
    url(
        r'^delete/$',
        views.SkillDeleteView.as_view(),
        name='delete_skill',
    ),
    url(
        r'^list/$',
        views.SkillListView.as_view(),
        name='list_skills',
    )
]