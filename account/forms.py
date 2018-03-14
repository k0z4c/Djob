from django import forms
from django.forms.models import model_to_dict
from .models import Profile
from authentication.models import User


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'img']

    def save(self, commit=True):
        if commit: self._replace_avatar_image()
        super(forms.ModelForm, self).save(commit)

    def _replace_avatar_image(self):
        profile = Profile.objects.get(user=self.instance.user)
        Profile.objects.check_and_delete_avatar_image(profile)

