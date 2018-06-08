from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from crispy_forms.helper import FormHelper
from .helpers import _decorate_name
from django.core.exceptions import ValidationError
from .validators import validate_invalid_chars
from .models import (
    Skill, SkillData
)

from crispy_forms.layout import (
    Submit, Layout, Fieldset, Field, HTML, Button, ButtonHolder
)

class SkillForm(forms.ModelForm):
    skill_name = forms.CharField(max_length=20, validators=[validate_invalid_chars,])

    def __init__(self, profile, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        self.profile = profile
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Fieldset(
                'Add a new skill to your profile',
                'skill_name',
                'description',
            )
        )

    class Meta:
        model = Skill
        fields =['description']

    def clean_skill_name(self):
        skill_name = _decorate_name(self.cleaned_data['skill_name'])
        if self.profile.skill_set.filter(data___codename=skill_name).exists():
            raise ValidationError(
                message='You already have %(skill)s in your skills.',
                params={'skill': self.cleaned_data['skill_name']},
                code='invalid'
            )
        return skill_name

    def save(self):
        (skill_data, created) = SkillData.objects.get_or_create(
            _codename=self.cleaned_data['skill_name']
            )
        self.instance.data = skill_data
        self.instance.profile = self.profile
        return super(SkillForm, self).save(commit=False)

class SkillMultipleSelectForm(forms.Form):

    data = forms.ModelMultipleChoiceField(
        label="Your skills",
        widget=CheckboxSelectMultiple,
        queryset=None
        )


    def __init__(self, user, *args, **kwargs):
        super(SkillMultipleSelectForm, self).__init__(*args, **kwargs)
        self.fields['data'].queryset = user.skill_set.filter()
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

