from django.shortcuts import render

from django.views.generic import edit
from django.views.generic import ListView

from .models import Skill, SkillData
from .forms import CreateSkillForm

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect 


# Create your views here.

def create_skill(request):
    if request.method == 'GET':
        form =  CreateSkillForm()
        return render(request, 'skiller/skill_form.html', {'form': form})
    elif request.method == 'POST':
        form = CreateSkillForm(request.POST)

        if form.is_valid():
            (skill, created) = Skill.manager.get_or_create(**form.cleaned_data)
            SkillData.objects.create(user=request.user, skill=skill)
            messages.success(request, 'success!', extra_tags='alert alert-success')
        else:
            messages.error(request, 'error', extra_tags='alert alert-danger')

        return redirect('account:profile_detail', request.user.email)

class SkillDeleteView(edit.DeleteView):
    model = Skill

class SkillListView(ListView):
    model = Skill

