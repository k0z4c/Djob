
from django.views.generic import ListView, edit
from django.contrib import messages
from django.views.generic.edit import ModelFormMixin
from django.urls import reverse, reverse_lazy
from .errors import DivErrorList
from django.core.exceptions import ValidationError

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
        ''' the form is valid so '''
        codename = form.cleaned_data['codename']
        skill_data = SkillData(_codename=codename)
        '''
            After form validation we have to do 
            instance validation on SkillData.
            If no errors, then we add the Skill
            association.
        '''
        try:
            skill_data.full_clean()
        except ValidationError as e:
            codename_errors = e.message_dict['_codename']
            for error_message in codename_errors:
                messages.error(
                    self.request,
                    message=error_message,
                    extra_tags='alert alert-danger'
                )
                return self.form_invalid(form)
        else:
            Skill.objects.add(self.request.user, name=codename)
            messages.success(
                self.request,
                message='Skill added successfully 😎',
                extra_tags='alert alert-success')

        return super(SkillAddView, self).form_valid(form)

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


