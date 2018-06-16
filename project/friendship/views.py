from .models import Friendship
from functools import reduce
from django.http import Http404
from django.http import JsonResponse
from marathon.models import SocialRequest
from django.shortcuts import get_object_or_404
from authentication.models import User 
from jsonview.decorators import json_view
from django.views.generic import (
  ListView, TemplateView
)

class FriendshipListView(ListView):
  model = Friendship

  @property
  def queryset(self):
    return self.model.objects.filter(
      by__user__email=self.kwargs.get('email')
      )

@json_view
def send_request(request, email):
  to = get_object_or_404(User, email=email)
  if to == request.user:
    raise Http404

  social_request = SocialRequest.objects.send_request(
    label='friendship_request',
    by=request.user.profile,
    to=to.profile,
    tile='{} has sended you a friendship request.'.format(request.user)
  )
  return JsonResponse({'message': 'request sended'})

# questo puo essere eliminato insieme al template
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

