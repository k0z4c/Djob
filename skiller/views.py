
from django.views.generic import ListView, edit, DetailView
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError

from .exceptions import DuplicatedSkill
from .errors import DivErrorList
from .models import (
    Skill, SkillData, Confirmation
)
from .forms import (
    SkillDataForm, SkillMultipleSelectForm
)

class SkillAddView(edit.FormView):
    template_name = 'skiller/skill_form.html'
    form_class = SkillDataForm

    @property
    def success_url(self):
        return reverse('account:profile_detail', args=((self.request.user.email,)))

    def form_valid(self, form):
        codename = form.cleaned_data['codename']
        skill_data = SkillData(codename=codename)
        if not (
            self._validate_input(skill_data) 
                and 
            self._insert_if_not_duplicated(skill_data.codename)
            ): 
            return self.form_invalid(form)

        messages.success(
            self.request,
            message='skills updated successfully',
            extra_tags='alert alert-success'
            )
        return super(edit.FormView, self).form_valid(form)

    def _validate_input(self, skill_data):
        try:
            skill_data.clean_fields()
        except ValidationError as e:
            for error_field in e.message_dict:
                for error in e.message_dict[error_field]:
                        messages.error(
                            self.request,
                            message=error,
                            extra_tags='alert alert-danger'
                        )
            return False
        return True

    def _insert_if_not_duplicated(self, codename):
        try:
            Skill.objects.add(
                profile=self.request.user.profile,
                name=codename
                )
        except DuplicatedSkill:
            messages.error(
                self.request,
                message='duplicated skill',
                extra_tags='alert alert-danger'
                )
            return False
        return True

    def get_form_kwargs(self):
        kwargs = super(SkillAddView, self).get_form_kwargs()
        kwargs.update({
            'error_class': DivErrorList,
            })
        return kwargs

class SkillDeleteView(edit.FormView):
    form_class = SkillMultipleSelectForm
    template_name = 'skiller/delete_form.html'
    success_url = reverse_lazy('skill:delete_skill')

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        qs = form.cleaned_data['data']
        for obj in qs: obj.delete()
        return super().form_valid(form) 

    def get_form_kwargs(self):
        kwargs = super(SkillDeleteView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
            })
        return kwargs

    
class SkillListView(ListView):
    model = Skill
    context_object_name = 'skills'

from marathon.models import SocialRequest
from authentication.models import User
class SuggestFormView(edit.FormView):
    form_class = SkillDataForm
    template_name = 'skiller/skill_form.html'

    def form_valid(self, form):
        try:
            to = User.objects.get(email=self.kwargs.get('email'))
        except User.DoesNotExist:
            pass

        SocialRequest.objects.send_request(
            by=self.request.user,
            to=to,
            label='skill_suggestion',
            tile='{} suggests you to add {} to your skills.'.format(self.request.user, form.cleaned_data['codename']),
            data={'codename': form.cleaned_data.get('codename')}
        )
        return super(edit.FormView, self).form_valid(form)
    @property
    def success_url(self):
        return reverse('account:profile_detail', args=[self.request.user,])

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from jsonview.decorators import json_view
from authentication.models import User
@json_view
def confirm_skill(request, email):
    skill = get_object_or_404(Skill, pk=request.POST.get('skill_pk'))
    user = User.objects.get(email=email)
    skill.confirmation_set.create(by=request.user, to=user, skill=skill)
    return JsonResponse({})

class SkillDetailView(DetailView):
    object_context_name = 'skill'
    model = Skill
