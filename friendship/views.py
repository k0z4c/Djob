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
from .models import Friendship, FriendshipRequest

from django.http import JsonResponse

class IndexView(generic.TemplateView):
    template_name = 'friendship/index.html'

class FriendshipListView(generic.list.ListView):
    model = Friendship
    context_object_name = 'friendships'
    def get_queryset(self):
        qs = self.request.user.contacts.all()
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            qs = qs.order_by(*ordering)
        return qs

class FriendshipRequestReceivedListView(generic.list.ListView):
    model = FriendshipRequest
    template_name = 'friendship/friendships_received.html'

    def get_queryset(self):
        qs = self.request.user.requests_received.all()
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            qs = qs.order_by(*ordering)
        return qs

class FriendshipRequestSentListView(generic.list.ListView):
    model = FriendshipRequest
    template_name = 'friendship/friendship_sent.html'

    def get_queryset(self):
        qs = self.request.user.requests_sent.all()
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            qs = qs.order_by(*ordering)
        return qs

def accept_request(request, pk):
    friendship_request = FriendshipRequest.objects.get(pk=pk)
    friendship_request.accept()
    messages.success(request, 'Request Accepted!')
    return HttpResponseRedirect(reverse('friendship:requests_received'))

def reject_request(request, pk):
    friendship_request = FriendshipRequest.objects.get(pk)
    friendship_request.reject()
    messages.success(request, 'Request Rejected!')
    return HttpResponseRedirect(request, reverse('friendship:requests_received', args=(pk,)))



# @login_required
def add_friendship_request(request):

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
    return HttpResponse('test!')

class addFriendshipRequestView(generic.View):
    def post(self):
        pass

def remove_friendship(request):
    to_user_id = request.POST.get('data', None)
    Friendship.objects.remove_friendship(request.user.id, to_user_id)
    print('removed?')
    response = { 'msg': 'received!'}
    return JsonResponse(response)

def friendship_notifications_count(request):
    # fetch unread requests 
    unread_requests = FriendshipRequest.objects.filter(
                        to=request.user.id,
                        read=False
                        ).count()

    response = { 'unread_notifications': unread_requests }
    return JsonResponse(response)


def friendship_notifications_list(request):
    unread_requests = FriendshipRequest.objects.filter(
        to=request.user.id,
        read=False,
        ).order_by('-date')[:3]

    data = { k: [v.by.email, v.date, v.by.get_absolute_url(), v.by.profile.img.url ] for k, v in enumerate(unread_requests)}
    print(data)
    return JsonResponse(data)

