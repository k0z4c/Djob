from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from crispy_forms.helper import FormHelper
from .models import (
    Skill, SkillData
)

from crispy_forms.layout import (
    Submit, Layout, Fieldset, Field, HTML, Button, ButtonHolder
)

class SkillDataForm(forms.Form):
    '''
        We can't use ModelForm because form.is_valid()
        triggered by the view will make model validation too
        ( we need to temporally separate these steps )
    '''
    error_css_class = 'alert alert-danger'

    codename = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        super(SkillDataForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, user, commit=True):
        skilldata = super(SkillDataForm, self).save(commit)
        Skill.objects.create(user=user, data=skilldata)
        return skilldata



class SkillMultipleSelectForm(forms.Form):

    data = forms.ModelMultipleChoiceField(
        label="Your skills",
        widget=CheckboxSelectMultiple,
        queryset=None
        )


    def __init__(self, user, *args, **kwargs):
        super(SkillMultipleSelectForm, self).__init__(*args, **kwargs)
        self.fields['data'].queryset = user.skill_set.filter()
        '''
        form style stuff
        '''
        self.helper = FormHelper()
        self.helper.field_class = 'skills-list'
        self.helper.form_id = 'form_skill_delete'
        self.helper.layout = Layout(
            Fieldset(
                '/remove skills',
                HTML("""
                    <p>Check skills you want to remove.</p>
                    """),
                Field('data'),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='btn btn-primary'),
                    Button('cancel', 'Cancel'),

                    ),
                ),
            )

