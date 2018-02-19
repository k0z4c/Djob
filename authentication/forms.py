
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import password_validation
from .models import User

# https://docs.djangoproject.com/en/1.11/ref/forms/validation/
# https://docs.djangoproject.com/en/1.11/ref/validators/#module-django.core.validators
from django.contrib.auth.forms import AuthenticationForm
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        max_length=200,
    )

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    class Meta:
        model = User
        fields = ['email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(error_messages['password_mismatch'], code='password_mismatch')
        # enable password default validators (settings.py)
        # when modelform initializes, it allocats an instance of the model
        # this is accessible by the instance attributes
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password2'))

        if commit:
            user.save()
        return user

# A form used in the admin interface to change a user’s information and permissions.
# https://docs.djangoproject.com/en/1.8/topics/auth/default/#django.contrib.auth.forms.UserChangeForm
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label = _("Password"),
        help_text = _(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"../password/\">this form</a>."
        )
    )
    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        return self.initial['password']
