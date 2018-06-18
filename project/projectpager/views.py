from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from notifications.signals import notify
from django.shortcuts import get_object_or_404

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
    return reverse('projectpager:project_detail', args=[self.request.user.email, self.object.pk,])

   def get_success_url(self):
    messages.success(
      self.request,
      message='Project page created successfully!',
      extra_tags='alert alert-success'
    )
    return super(ProjectPageCreateView, self).get_success_url()

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
    messages.success(
      self.request,
      message='invite sended!',
      extra_tags='alert alert-success'
    )
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

class ProjectPageDetailView(ListView):
  model = ProjectPage
  pk_url_kwarg = 'project_pk'
  context_object_name = 'threads'
  template_name = 'projectpager/projectpage_detail.html'
  paginate_by = 5

  def get_queryset(self):
    project = get_object_or_404(ProjectPage, pk=self.kwargs.get('project_pk'))
    return Thread.objects.filter(project__pk=project.pk)

  def get_context_data(self):
    context = super(ProjectPageDetailView, self).get_context_data()
    context.update({
      'projectpage': ProjectPage.objects.get(pk=self.kwargs.get('project_pk')),
    })
    return context

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

  def get_success_url(self):
    messages.success(
      self.request,
      message='project attributes successfully updated',
      extra_tags='alert alert-success'
    )
    return super(ProjectPageUpdateView, self).get_success_url()
  
class ThreadCreateView(UserPassesTestMixin, CreateView):
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
      args=[self.request.user.email, self.object.project.pk]
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

  def form_valid(self, form):
    for profile in self.object.discussion.project.profiles.exclude(pk=self.request.user.profile.pk):
      notify.send(
        sender=self.request.user,
        recipient=profile.user,
        verb='thread_message_reply',
        description='{} has replied to {} thread in {}'.format(
          self.request.user, self.object.discussion.title, self.object.discussion.project.name
        )
      )

      return super(MessageCreateView, self).form_valid(form)

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

