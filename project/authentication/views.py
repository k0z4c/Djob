from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import views
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import (
    UserCreationForm, CustomAuthenticationForm
)
from django.views.generic import (
    CreateView, TemplateView
)

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        response = super(CustomLoginView, self).form_valid(form)
        first_access = self.request.user.first_access
        self.request.session['just_logged_in'] = True
        return response if not first_access else redirect('account:profile_edit', self.request.user)

class SignupView(CreateView):
    model = settings.AUTH_USER_MODEL
    form_class = UserCreationForm
    template_name = 'registration/signin.html'

    @property
    def success_url(self):
        return reverse('authentication:thanks')
    
class ThanksView(TemplateView):
    template_name = 'registration/thanks.html'
