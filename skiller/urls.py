from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^add/$',
        views.SkillAddView.as_view(),
        name='add_skill',
    ),
    url(
        r'^(?P<email>([\w\.\+\-])+@(\w)+\.(\w)+)/suggest/$',
        views.SuggestFormView.as_view(),
        name='suggest_skill'
    ),
    url(
        r'^ajax/(?P<email>([\w\.\+\-])+@(\w)+\.(\w)+)/confirm/$',
        views.confirm_skill,
        name='confirm_skill'
    ),
    url(
        r'^(?P<pk>(\d+))/detail/$',
        views.SkillDetailView.as_view(),
        name='skill_detail'
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