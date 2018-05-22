from django.shortcuts import render

from django.views import generic

from .models import Profile
# Create your views here.

from django.shortcuts import get_object_or_404
from authentication.models import User
from django.urls import reverse
from django.shortcuts import redirect
from .models import Profile
from .forms import ProfileEditForm
from django.http import HttpResponseRedirect

from authentication.forms import UserEditForm
from guardian.mixins import PermissionRequiredMixin, LoginRequiredMixin
from friendship.models import Friendship
from django.db.models import Q

def index(request):
    '''
    redirects to profile detail view.
    '''
    profile = get_object_or_404(Profile, user__email=request.user.email)
    return redirect(profile, permanent=True)

class ProfileDetailView(LoginRequiredMixin, generic.detail.DetailView):
    '''
    Renders the profile requested by URL.
    '''
    model = Profile

    def get_object(self, queryset=None):
        if self.request.user.email == self.kwargs.get('email'):
            return self.request.user.profile

        user = get_object_or_404(
            User,
            email=self.kwargs.get('email')
        )
        return user.profile

    def _is_owner(self):
        return self.request.user.email == self.kwargs.get('email')

    def get_context_data(self, **kwargs):
        if self._is_owner():
            kwargs.update({
                'owner': True,
                'friends': Friendship.objects.get_friends(self.request.user),
            })
        else:
            user_visited = User.objects.get(email=self.kwargs['email'])
            if Friendship.objects.are_friends(self.request.user, user_visited):
                kwargs.update({'friends': True})

        kwargs.update({
            'first_skills': self.request.user.skill_set.all()[:5]
            })
        return super(ProfileDetailView, self).get_context_data(**kwargs)

class EditAccountView(LoginRequiredMixin, PermissionRequiredMixin, generic.base.TemplateResponseMixin, generic.base.View):
    '''
    *_keys are form's fields which are used to split
    fields in POST request.
    '''

    template_name = 'account/profile_update_form.html'
    success_url = 'account:profile_detail'
    user_keys = ['email', 'first_name', 'last_name']
    profile_keys = ['description']

    permission_required = 'account.can_change_profile'
    return_403 = True

    @classmethod
    def check_and_save(cls, f1, f2):
        if f1.is_valid() and f2.is_valid():
            f1.save() and f2.save()

    def get_permission_object(self):
        obj = Profile.objects.get(user__email=self.kwargs.get('email'))
        return obj

    def post(self, request, *args, **kwargs):

        user_data = { k: request.POST[k] for k in self.user_keys }
        profile_data = { k: request.POST[k] for k in self.profile_keys }

        f1 = UserEditForm(user_data, instance=request.user)
        f2 = ProfileEditForm(profile_data, request.FILES, instance=request.user.profile)
        self.check_and_save(f1, f2)

        return HttpResponseRedirect(reverse(self.success_url,
                                            args=[request.user.email]))

    def get(self, request, *args, **kwargs):
        f1 = UserEditForm(instance=request.user)
        f2 = ProfileEditForm(instance=request.user.profile)
        return self.render_to_response({'f1': f1, 'f2': f2})


from django.core.paginator import Paginator
class MyPaginator(Paginator):
  def page(self, number):
    number = self.validate_number(number)
    bottom = (number - 1) * self.per_page
    top = bottom + self.per_page
    if top + self.orphans >= self.count:
        top = self.count
    '''custom behaviour'''
    object_page_list = self.object_list[bottom:top]
    for notification in object_page_list: notification.mark_as_read()
    return self._get_page(object_page_list, number, self)

from django.views.generic import ListView
from notifications.models import Notification
# UnreadNotificationsListView
class UnreadedNotificationsListView(ListView):
  model = Notification
  template_name = 'account/notifications.html'
  paginate_by = 5
  paginator_class = MyPaginator
  # context_object_name = 'unreaded_notifications_list'

  @property
  def queryset(self):
    return Notification.objects.filter(recipient=self.request.user).unread()

  def get_context_data(self, **kwargs):
    return super(UnreadedNotificationsListView, self).get_context_data(
        unread=True,
        **kwargs
        )

class ReadedNotificationsListView(ListView):
    model = Notification
    template_name = 'account/notifications.html'
    paginate_by = 5
    paginator_class = MyPaginator
    # context_object_name = 'readed_notifications_list'

    @property
    def queryset(self):
        return Notification.objects.filter(recipient=self.request.user).read()
    def get_context_data(self, **kwargs):
        return super(ReadedNotificationsListView, self).get_context_data(
            unread=False,
            **kwargs
            )

