from django import forms
from django.forms.models import model_to_dict
from .models import Profile
from authentication.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Submit
)
from django.core.files.uploadedfile import UploadedFile
from django.conf import settings

import os
from .fields import AvatarImageFieldFile

class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['img'].label = 'Avatar'
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Profile
        fields = ['actual_job', 'description', 'img']

    def clean_img(self):
        file = self.cleaned_data.get('img')
        if isinstance(file, UploadedFile):
            file_path = os.path.join(
                settings.MEDIA_ROOT, str(self.instance.id),  str(file)
            )
            if os.path.isfile(file_path):
                return os.path.join(str(self.instance.id), str(file))
            return self.cleaned_data.get('img')

        elif isinstance(file, AvatarImageFieldFile):
            return False

        return self.instance.img

    def clean(self):
        print("clear: ", self.cleaned_data['img'])
        return self.cleaned_data
