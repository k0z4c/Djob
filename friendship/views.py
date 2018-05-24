from django.shortcuts import render
from django.views.generic import (
  ListView, TemplateView
)

from .models import Friendship
from marathon.models import SocialRequest

from django.http import JsonResponse
from authentication.models import User 

from notifications.signals import notify
# Create your views here.

class FriendshipListView(ListView):
  model = Friendship

  @property
  def queryset(self):
    return self.model.objects.filter(
      by__user__email=self.kwargs.get('email')
      )

''' send_request'''
def send_request(request, email):
  try:
    to = User.objects.get(email=email)
  except User.DoesNotExist:
    pass

  social_request = SocialRequest.objects.send_request(
    label='friendship_request',
    by=request.user,
    to=to,
    tile='{} has sended you a friendship request.'.format(request.user)
  )
  return JsonResponse({'message': 'request sended'})

class FriendshipRequestList(TemplateView):
  template_name = 'friendship/friendship_pending_list.html'
