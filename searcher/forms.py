from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Submit
)
from skiller.models import SkillData

class SearchForm(forms.Form):

  def __init__(self, *args, **kwargs):
    super(SearchForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.add_input(Submit('submit', 'Submit'))
    self.fields['skill_serial'].queryset = SkillData.objects.all()

  email = forms.CharField(max_length=30, required=False)
  first_name = forms.CharField(max_length=30, required=False)
  last_name = forms.CharField(max_length=30, required=False)

  skill_serial = forms.ModelChoiceField(queryset=None, required=False)
  project_name = forms.CharField(max_length=30, required=False)

  def clean_skill_serial(self):
    value = self.cleaned_data['skill_serial']
    if value:
      value = self.cleaned_data['skill_serial'].serial
    return value

  def clean(self):
    not_null_fields = { k: v for k, v in self.cleaned_data.items() if v }
    return not_null_fields
