from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from crispy_forms.helper import FormHelper
from .helpers import _decorate_name
from django.core.exceptions import ValidationError
from django.db.models import Q
from marathon.models import SocialRequest
from .validators import validate_invalid_chars
from .models import (
    Skill, SkillData
)

from crispy_forms.layout import (
    Submit, Layout, Fieldset, Field, HTML, Button, ButtonHolder
)

class SuggestSkillForm(forms.Form):
    codename = forms.CharField(max_length=20,  label='skill to suggest')

    def __init__(self, *args, **kwargs):
        self.suggest_to = kwargs.pop('to')
        self.by = kwargs.pop('by')
        super(SuggestSkillForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('suggest', 'Suggest'))

    def clean_codename(self):
        decorated_codename = _decorate_name(self.cleaned_data['codename'])
        if self.suggest_to.skill_set.filter(data___codename=decorated_codename).exists():
            raise ValidationError(
                '%(user)s has already this skill!',
                params={'user': self.suggest_to.user.email},
                code='invalid'
            )
        return decorated_codename

    def clean(self):
        cleaned_data = super(SuggestSkillForm, self).clean()
        if cleaned_data.get('codename', None):
            lookup_fields = Q(
                label='skill_suggestion',
                by=self.by,
                data={'codename': cleaned_data['codename']},
                status=SocialRequest.PENDING
            )
            if self.suggest_to.marathon_received.filter(lookup_fields).exists():
                raise ValidationError(
                    'You have already suggested this skill; your request is in pending',
                    code='invalid'
                )

class SkillForm(forms.ModelForm):
    skill_name = forms.CharField(max_length=20)

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
                params={'skill': self.cleaned_data['skill_name'].lower()},
                code='invalid'
            )
        return skill_name

    def save(self):
        (skill_data, created) = SkillData.objects.get_or_create(
            _codename=self.cleaned_data['skill_name']
            )
        self.instance.data = skill_data
        self.instance.profile = self.profile
        return super(SkillForm, self).save()

