
from django.views.generic import ListView, edit
from django.contrib import messages
from django.views.generic.edit import ModelFormMixin
from django.urls import reverse 

from .models import Skill, SkillData
from .forms import SkillDataForm
from .errors import DivErrorList

class SkillAddView(edit.CreateView):
    model = SkillData
    form_class = SkillDataForm

    @property
    def success_url(self):
        return reverse('account:profile_detail', args=((self.request.user.email,)))

    def form_valid(self, form):
        self.object = form.save(self.request.user)
        messages.success(self.request, 'success!', extra_tags='alert alert-success')
        return super(ModelFormMixin, self).form_valid(form)
        
    def form_invalid(self, form):
        return super(ModelFormMixin, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(SkillAddView, self).get_form_kwargs()
        kwargs.update({
            'error_class': DivErrorList,
            })
        return kwargs
  
class SkillDeleteView(edit.DeleteView):
    pass
#     model = Skill

class SkillListView(ListView):
    pass
#     model = Skill



