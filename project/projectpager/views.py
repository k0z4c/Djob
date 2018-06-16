from django.urls import reverse
from django.http import HttpResponseRedirect
from guardian.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import (
  CreateView, ListView, DetailView, UpdateView, FormView
)
from .forms import (
  CreateProjectPageForm, ThreadForm, MessageForm, InviteForm, UpdateProjectPageForm
)
from .models import (
  ProjectPage, Thread, Message
)


class ProjectPageCreateView(CreateView):
   model = ProjectPage
   form_class = CreateProjectPageForm

   @property
   def success_url(self):
    return reverse('account:profile_detail', args=[self.request.user,])

   def get_form_kwargs(self):
    kwargs = super(ProjectPageCreateView, self).get_form_kwargs()
    kwargs.update({
      'profile': self.request.user.profile,
      })
    return kwargs

class InviteRequestFormView(FormView):
  form_class = InviteForm
  template_name = 'projectpager/invite_form.html'

  @property
  def success_url(self):
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
  pk_url_kwarg = 'project_pk'

class ProjectPageUpdateView(UserPassesTestMixin, UpdateView):
  model = ProjectPage
  form_class = UpdateProjectPageForm
  pk_url_kwarg = 'project_pk'

  def test_func(self):
    project_page = self.get_object()
    return project_page.owner == self.request.user.profile
    
  @property
  def success_url(self):
    return reverse(
      'projectpager:project_detail',
      args=[self.request.user.email, self.kwargs['project_pk']]
    )
  
class ThreadCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Thread
  form_class = ThreadForm
  raise_exception = True

  def test_func(self):
    project = ProjectPage.objects.get(pk=self.kwargs['project_pk'])
    return self.request.user.has_perm('can_open_threads', project)

  @property
  def success_url(self):
    return reverse(
      'projectpager:project_detail',
      args=[self.request.user.email, self.kwargs['project_pk']]
    )


  def get_form_kwargs(self):
    kwargs = super(ThreadCreateView, self).get_form_kwargs()
    kwargs.update({
      'profile': self.request.user.profile,
      'project': ProjectPage.objects.get(pk=self.kwargs['project_pk']),
    })
    return kwargs

class ThreadDetailView(DetailView):
  model = Thread
  pk_url_kwarg = 'thread_pk'

class MessageCreateView(UserPassesTestMixin, CreateView):
  model = Message
  form_class = MessageForm
  raise_exception = True

  def test_func(self):
    project = ProjectPage.objects.get(pk=self.kwargs['project_pk'])
    return self.request.user.has_perm('can_open_threads', project)

  @property
  def success_url(self):
    return reverse(
      'projectpager:thread_detail',
      args=[self.request.user.email, self.kwargs['project_pk'], self.kwargs['thread_pk']]
      )
  
  def get_form_kwargs(self):
    kwargs = super(MessageCreateView, self).get_form_kwargs()
    kwargs.update({
      'profile': self.request.user.profile,
      'thread': Thread.objects.get(pk=self.kwargs['thread_pk'])
    })
    return kwargs

