from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, FormView
from .models import ProjectPage, Thread, Message
from .forms import CreateProjectPageForm, ThreadForm, MessageForm
from django.http import HttpResponseRedirect
from django.urls import reverse

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

from django.views.generic import CreateView
from .forms import InviteForm
from marathon.models import SocialRequest

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

class ProjectPageUpdateView(UpdateView):
  model = ProjectPage
  form_class = CreateProjectPageForm

class ThreadCreateView(CreateView):
  model = Thread
  form_class = ThreadForm

  @property
  def success_url(self):
    # print(reverse('projectpager:detail', args=[self.request.user.email, self.kwargs.get('pk')]))
    print(self.object)
    return reverse(
      'projectpager:detail',
      args=[self.request.user.email, self.kwargs['pk']]
    )
  
  def get_form_kwargs(self):
    kwargs = super(ThreadCreateView, self).get_form_kwargs()
    kwargs.update({
      'profile': self.request.user.profile,
      'project': ProjectPage.objects.get(pk=self.kwargs['pk']),
    })
    return kwargs

class ThreadDetailView(DetailView):
  model = Thread
  pk_url_kwarg = 'thread_pk'

class MessageCreateView(CreateView):
  model = Message
  form_class = MessageForm

  @property
  def success_url(self):
    return reverse(
      'projectpager:thread_detail',
      args=[self.request.user.email, self.kwargs['pk'], self.kwargs['thread_pk']]
      )
  
  def get_form_kwargs(self):
    kwargs = super(MessageCreateView, self).get_form_kwargs()
    kwargs.update({
      'profile': self.request.user.profile,
      'thread': Thread.objects.get(pk=self.kwargs['thread_pk'])
    })
    return kwargs

