from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import views
from django.shortcuts import render
from django.conf import settings
from .forms import (
    UserCreationForm, CustomAuthenticationForm
)
from django.views.generic import (
    CreateView, TemplateView
)

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


class SignupView(CreateView):
    model = settings.AUTH_USER_MODEL
    form_class = UserCreationForm
    template_name = 'registration/signin.html'

    @property
    def success_url(self):
        return reverse('authentication:thanks')
    
class ThanksView(TemplateView):
    template_name = 'registration/thanks.html'
