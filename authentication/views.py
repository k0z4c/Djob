from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
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

    def form_valid(self, form):
        response = super(CustomLoginView, self).form_valid(form)
        self.request.session['just_logged_in'] = True
        return response

class CustomLogoutView(LogoutView):
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        self._check_first_access()
        return super(CustomLogoutView, self).dispatch(request, *args, **kwargs)

    def _check_first_access(self):
        user = self.request.user
        if user.first_access:
            user.first_access = False
            user.save()

class SignupView(CreateView):
    model = settings.AUTH_USER_MODEL
    form_class = UserCreationForm
    template_name = 'registration/signin.html'

    @property
    def success_url(self):
        return reverse('authentication:thanks')
    
class ThanksView(TemplateView):
    template_name = 'registration/thanks.html'
