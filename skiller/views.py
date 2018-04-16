
from django.views.generic import ListView, edit
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError

from .exceptions import DuplicatedSkill
from .errors import DivErrorList
from .models import (
    Skill, SkillData
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
                user=self.request.user,
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

