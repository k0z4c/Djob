from django import forms
from .models import ProjectPage, Thread, Message
from django.core import serializers
from crispy_forms.helper import FormHelper
from marathon.models import SocialRequest
from helpers import _decorate_name
from crispy_forms.layout import (
  Submit,
)

class InviteForm(forms.Form):
  project = forms.ModelChoiceField(queryset=None)
  to = forms.ModelMultipleChoiceField(queryset=None)

  def __init__(self, profile, *args, **kwargs):
    super(InviteForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.add_input(Submit('submit', 'Submit'))

    self.profile = profile
    self.fields['project'].queryset = profile.projectpages.filter(owner=profile)
    self.fields['to'].queryset = profile.contacts.all()

  def clean(self):
    project = self.cleaned_data['project']
    recipients = self.cleaned_data['to']

    from django.core.exceptions import ValidationError
    qs = recipients.filter(to__projectpages=project) 
    if qs.exists():
      raise ValidationError(
        message='%(users)s already member of this project',
        params={'users': ' '.join([q.to.user.email for q in qs])},
        code='invalid'
      )

  def save(self, commit=False):
    if self.errors:
        raise ValueError(
            "The %s could not be %s because the data didn't validate." % (
                self.instance._meta.object_name,
                'created' if self.instance._state.adding else 'changed',
            )
        )
    invites = []
    qs = self.cleaned_data['to']
    for friendship in qs:
      invites.append(
        SocialRequest.objects.send_request(
          label='invite_request',
          tile='{} invites you to join {} group.'.format(
            self.profile.user.email,
            self.cleaned_data['project'].name
            ),
          by=self.profile,
          to=friendship.to,
          data={'project': serializers.serialize('json', [self.cleaned_data['project']])}
        )
      )
    return invites

class UpdateProjectPageForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(UpdateProjectPageForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.add_input(Submit('update', 'Update'))

  class Meta:
    model = ProjectPage
    fields = ['_name', 'description']

class CreateProjectPageForm(forms.ModelForm):
  invite_all_contacts = forms.BooleanField(initial=False, widget=forms.CheckboxInput, required=False)

  class Meta:
    model = ProjectPage
    fields = ['_name', 'description']

  def __init__(self, profile, *args, **kwargs):
    super(CreateProjectPageForm, self).__init__(*args, **kwargs)
    self.profile = profile
    self.helper = FormHelper()
    self.helper.add_input(Submit('submit', 'Submit'))

  def clean__name(self):
    name = self.cleaned_data['_name']
    if name:
      name = _decorate_name(name)
    return name

  def save(self, **kwargs):
    self.instance.owner = self.profile
    project_page = super(CreateProjectPageForm, self).save(**kwargs)

    if self.cleaned_data['invite_all_contacts']:
      for p in self.profile.contacts.all():
        SocialRequest.objects.send_request(
          label='invite_request',
          tile='{} invites you to join {} group.'.format(
            self.profile.user.email,
            self.cleaned_data['name']
            ),
          by=self.profile,
          to=p.to,
          data={'project': serializers.serialize('json', [project_page])}
        )
    return project_page

class ThreadForm(forms.ModelForm):
  def __init__(self, profile, project, *args, **kwargs):
    super(ThreadForm, self).__init__(*args, **kwargs)
    self.profile = profile
    self.project = project
    self.helper = FormHelper()
    self.helper.add_input(Submit('submit', 'Submit'))

  class Meta:
    model = Thread
    fields = ['title', 'description']

  def save(self):
    thread = super(ThreadForm, self).save(commit=False)
    thread.project = self.project
    thread.created_by = self.profile
    thread.save()
    return thread


class MessageForm(forms.ModelForm):
  def __init__(self, profile, thread, *args, **kwargs):
    super(MessageForm, self).__init__(*args, **kwargs)
    self.profile = profile 
    self.thread = thread
    self.fields['body'].label = 'message'
    self.helper = FormHelper()
    self.helper.add_input(Submit('submit', 'Submit'))

  class Meta:
    model = Message
    fields = ['body',]

  def save(self):
    message = super(MessageForm, self).save(commit=False)
    message.discussion = self.thread
    message.posted_by = self.profile
    message.save()
    return message