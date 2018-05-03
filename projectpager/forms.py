from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
  Submit,
)

from .models import ProjectPage
#  real model form -> create invite; createview? 
class InviteForm(forms.ModelForm):
  pass

# maybe update view? 
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