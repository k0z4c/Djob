from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
  Submit,
)

from .models import ProjectPage

from marathon.models import SocialRequest

class InviteForm(forms.Form):
  group = forms.ModelChoiceField(queryset=None)
  to = forms.ModelMultipleChoiceField(queryset=None, required=False)

  def __init__(self, profile, *args, **kwargs):
    super(InviteForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.add_input(Submit('submit', 'Submit'))

    self.profile = profile
    self.fields['group'].queryset = profile.projectpages.all()
    self.fields['to'].queryset = profile.contacts.all()

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
            self.cleaned_data['group'].name
            ),
          by=self.profile,
          to=friendship.to,
          data={}
        )
      )
    return invites

class UpdateProjectPageForm(forms.ModelForm):
  pass

# Create View create view?
class CreateProjectPageForm(forms.ModelForm):
  class Meta:
    model = ProjectPage
    fields = ['name', 'description']

  def __init__(self, *args, **kwargs):
    super(CreateProjectPageForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.add_input(Submit('submit', 'Submit'))

  def save(self, user, *args, **kwargs):
    '''
      we have to save the instance before
      set manytomanyfield (users)
    '''
    self.instance.owner = user.profile
    project_page = super(CreateProjectPageForm, self).save(*args, **kwargs)
    if not kwargs.get('commit', ''):
      project_page.profiles.add(user.profile)
      project_page = super(CreateProjectPageForm, self).save(*args, **kwargs)
    return project_page
