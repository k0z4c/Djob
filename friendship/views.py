from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

from .models import FriendshipRequest, Friendship
from authentication.models import User
from .exceptions import FriendshipExists
from django.shortcuts import get_object_or_404
from .exceptions import FriendshipRequestExists

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from django.contrib import messages
from notifications.signals import notify

# @login_required
def add_friendship_request(request):
    ''' user can make a request to others
    only if it isnt a friend or has a suspended
    request
    # this https://github.com/django-notifications/django-notifications
    '''
    if request.method == 'POST':
        to_email = request.POST.get('email')
        to = get_object_or_404(User, email=to_email)
        try:
            FriendshipRequest.objects.send_request(by=request.user, to=to)
        except FriendshipRequestExists:
            pass
        # raise a notification to user
        messages.success(request, 'Request sended!')
        # raise notification to user to_email
        notify.send(request.user, recipient=to, verb='has sent you a request.')
        return HttpResponseRedirect(reverse('account:profile_detail', args=[to_email]))
    # error message
    return HttpResponse('boh!')

def accept_request(request):
    # by = User.objects.get(email=request.POST['by'])
    # print(by)
    # friendship_request = FriendshipRequest.objects.get(by=by, to=request.user)
    # friendship_request.accept_request()
    #
    # return HttpResponse('friendship accepted!')
    pass

class addFriendshipRequestView(generic.View):
    def post(self):
        pass
