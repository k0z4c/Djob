from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from jsonview.decorators import json_view
from authentication.models import User
from recommander.models import Activity
from marathon.models import SocialRequest
from .errors import DivErrorList
from django.contrib import messages
from helpers import get_decorated_name
from django.views.generic import (
    ListView, edit, DetailView
)
from .models import (
    Skill
)
from .forms import (
    SkillForm, SuggestSkillForm
)

class SkillAddView(edit.CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'skiller/skill_form.html'

    @property
    def success_url(self):
        return reverse('account:profile_detail', args=((self.request.user.email,)))

    def get_form_kwargs(self):
        kwargs = super(SkillAddView, self).get_form_kwargs()
        kwargs.update({
            'profile': self.request.user.profile,
            'error_class': DivErrorList,
            })
        return kwargs

class SkillListView(ListView):
    model = Skill
    context_object_name = 'skills'

class SuggestFormView(edit.FormView):
    form_class = SuggestSkillForm
    template_name = 'skiller/suggest_skill_form.html'

    def form_valid(self, form):
        try:
            to = User.objects.get(email=self.kwargs.get('email'))
        except User.DoesNotExist:
            pass

        SocialRequest.objects.send_request(
            by=self.request.user.profile,
            to=to.profile,
            label='skill_suggestion',
            tile='{} suggests you to add {} to your skills.'.format(self.request.user, form.cleaned_data['codename']),
            data={'codename': get_decorated_name(form.cleaned_data.get('codename'))}
        )
        messages.success(
            self.request,
            'skill successfull sended to {}'.format(to),
            extra_tags='alert alert-success',
        )
        return super(edit.FormView, self).form_valid(form)
    @property
    def success_url(self):
        return reverse('account:profile_detail', args=[self.request.user,])

    def get_form_kwargs(self):
        kwargs = super(SuggestFormView, self).get_form_kwargs()
        kwargs.update({
            'to': User.objects.get(email=self.kwargs.get('email')).profile,
            'by': self.request.user.profile,
            'error_class': DivErrorList
        })
        return kwargs

@json_view
def confirm_skill(request, email):
    skill = get_object_or_404(Skill, pk=request.POST.get('skill_pk'))
    user = User.objects.get(email=email)
    response = {}
    if skill.confirmation_set.filter(by=request.user, to=user, skill=skill).exists():
        response.update({'status': 'error', 'message': 'You have already confirmed this skill'})
    else:
        skill.confirmation_set.create(by=request.user, to=user, skill=skill)
        request.user.profile.activities.create(profile=user.profile, activity_type=Activity.SKILL_CONFIRMED)
        response.update({'status': 'success', 'message': 'Skill confirmed successfully'})
    return JsonResponse(response)

@json_view
def delete_skill(request, email):
    skill = get_object_or_404(Skill, pk=request.POST.get('skill_pk'), profile=request.user.profile)
    skill.delete()
    return JsonResponse({'status': 'success', 'message': 'Skill successfully removed'})

class SkillDetailView(DetailView):
    object_context_name = 'skill'
    model = Skill
