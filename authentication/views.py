from django.shortcuts import render
from django.contrib.auth import views
from .forms import UserCreationForm, CustomAuthenticationForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.views import LoginView
class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

def signup(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email_user(
                'Subject',
                'Email Body',
                from_email='example@socialnetwork.info'
            )
            return HttpResponseRedirect('/thanks/')

    elif request.method == 'GET':
        form = UserCreationForm()

    return render(request, 'registration/signin.html', {'form': form})

# after successful login redirect; for further auth methods e.g two factor
def checkpoint(request):
    email = request.user.email
    return HttpResponseRedirect(reverse('account:get_profile', args=[email]))
