from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, FormView
from .models import ProjectPage
from .forms import CreateProjectPageForm
from django.http import HttpResponseRedirect
from django.urls import reverse

class ProjectPageCreateView(CreateView):
   model = ProjectPage
   form_class = CreateProjectPageForm

   @property
   def success_url(self):
    return reverse('account:profile_detail', args=[self.request.user,])

   def form_valid(self, form):
      self.object = form.save(self.request.user)
      return HttpResponseRedirect(self.get_success_url())

from django.views.generic import CreateView
from .forms import InviteForm
from marathon.models import SocialRequest

class InviteRequestFormView(FormView):
  form_class = InviteForm
  # to change
  template_name = 'projectpager/invite_form.html'

  @property
  def success_url(self):
    from django.urls import reverse
    return reverse('account:profile_detail', args=[self.request.user.email,])
  
  def form_valid(self, form):
    self.object = form.save()
    return HttpResponseRedirect(self.get_success_url())

  def form_invalid(self, form):
    return super(InviteRequestFormView, self).form_invalid(form)
  def get_form_kwargs(self):
    kwargs = super(InviteRequestFormView, self).get_form_kwargs()
    kwargs.update({
      'profile': self.request.user.profile,
      })
    return kwargs


class ProjectPageListView(ListView):
  model = ProjectPage

  @property
  def queryset(self):
    user_email = self.kwargs.get('email')
    return self.model.objects.filter(profiles__user__email=user_email)

class ProjectPageDetailView(DetailView):
  model = ProjectPage

class ProjectPageUpdateView(UpdateView):
  model = ProjectPage
  form_class = CreateProjectPageForm