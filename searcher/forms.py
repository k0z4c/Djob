from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Submit , Button
)
from skiller.models import SkillData

class SearchForm(forms.Form):

  def __init__(self, *args, **kwargs):
    super(SearchForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_id = 'searchForm'
    self.helper.add_input(Submit('submit', 'Submit'))
    self.helper.add_input(Button('formReset', 'Reset', css_class='btn btn-primary'))

    self.fields['skill_serial1'].queryset = SkillData.objects.all()
    self.fields['skill_serial2'].queryset = SkillData.objects.all()

  email = forms.CharField(max_length=30, required=False)
  first_name = forms.CharField(max_length=30, required=False)
  last_name = forms.CharField(max_length=30, required=False)

  skill_serial1 = forms.ModelChoiceField(queryset=None, required=False, empty_label='')
  skill_serial2 = forms.ModelChoiceField(queryset=None, required=False, empty_label='')

  project_name = forms.CharField(max_length=30, required=False)

  def clean_skill_serial1(self):
    value = self.cleaned_data['skill_serial1']
    if value:
      value = self.cleaned_data['skill_serial1'].serial
    return value

  def clean_skill_serial2(self):
    value = self.cleaned_data['skill_serial2']
    if value:
      value = self.cleaned_data['skill_serial2'].serial
    return value

  def clean(self):
    not_null_fields = { k: v for k, v in self.cleaned_data.items() if v }
    return not_null_fields
