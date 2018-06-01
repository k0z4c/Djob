from django.shortcuts import render
from django.views.generic import (
  ListView, TemplateView
)

from .models import Friendship
from marathon.models import SocialRequest

from django.http import JsonResponse
from authentication.models import User 

from notifications.signals import notify
from django.db.models import Count
from functools import reduce

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
    by=request.user.profile,
    to=to.profile,
    tile='{} has sended you a friendship request.'.format(request.user)
  )
  return JsonResponse({'message': 'request sended'})

class FriendshipRequestList(TemplateView):
  template_name = 'friendship/friendship_pending_list.html'

class NetworkList(ListView):
    model = Friendship
    context_object_name = 'contacts_ordered_by_friends_list'
    template_name = 'friendship/ordered_by_friends_list.html'

    @property
    def queryset(self):
      user_friendships = self.model.objects.filter(by__user__email=self.kwargs.get('email'))
      qs = user_friendships.order_by('-to__num_contacts')
      return qs
    
    def get_context_data(self, **kwargs):
      counting_func = lambda x, y: x.to.num_contacts + y.to.num_contacts
      second_level_neighbors_count = reduce(counting_func, self.object_list)

      kwargs.update({
        'first_level_neighbors_count': self.object_list.count(),
        'second_level_neighbors_count': second_level_neighbors_count
      })
      return super(NetworkList, self).get_context_data(**kwargs)

