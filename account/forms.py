from django import forms
from django.forms.models import model_to_dict
from .models import Profile
from authentication.models import User


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'img']

    # def clean_img(self):
    #     from io import BytesIO
    #     from PIL import Image
    #     from copy import copy
    #
    #     cleaned_data = copy(self.cleaned_data['img']) # django.core.files.uploadefile.InMemoryUploadedFile
    #     # bytesio object
    #     img = Image.open(cleaned_data)
    #     cleaned_data.file = BytesIO(img.tobytes())
    #     print('returning')
    #     return cleaned_data
