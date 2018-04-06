from django.shortcuts import render

from django.views.generic import edit
from django.views.generic import ListView

from .models import Skill, SkillData
# from .forms import CreateSkillForm
from .forms import SkillDataForm

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect 

from .exceptions import DuplicatedSkill
# Create your views here.

def add_skill(request):
    if request.method == 'GET':
        form =  SkillDataForm()
        return render(request, 'skiller/skill_form.html', {'form': form})
    elif request.method == 'POST':
        form = SkillDataForm(request.POST)
        if form.is_valid():
            try:
                Skill.objects.add_skill(request.user, form.cleaned_data['codename'])
            except DuplicatedSkill:
                messages.error(request, 'You have yet this skill', extra_tags='alert alert-danger')
            else:
                messages.success(request, 'success!', extra_tags='alert alert-success')
        else:
            messages.error(request, 'The form is not valid', extra_tags='alert alert-danger')

        return redirect('account:profile_detail', request.user.email)

class SkillDeleteView(edit.DeleteView):
    pass
#     model = Skill

class SkillListView(ListView):
    pass
#     model = Skill



