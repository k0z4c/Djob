from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from .models import ProjectPage
from .forms import CreateProjectPageForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
class ProjectPageCreateView(CreateView):
   model = ProjectPage
   form_class = CreateProjectPageForm

   @property
   def success_url(self):
    return reverse('account:profile_detail', args=[self.request.user,])

   def form_valid(self, form):
      self.object = form.save(self.request.user)
      return HttpResponseRedirect(self.get_success_url())

class ProjectPageListView(ListView):
  model = ProjectPage

  '''must list projects that i joined'''
  @property
  def queryset(self):
    return self.request.user.projectpages.all()

class ProjectPageDetailView(DetailView):
  model = ProjectPage

class ProjectPageUpdateView(UpdateView):
  model = ProjectPage
  form_class = CreateProjectPageForm