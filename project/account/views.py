from django.shortcuts import render
from django.views import generic
from .models import Profile
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect
from .models import Profile
from .forms import ProfileEditForm
from django.http import HttpResponseRedirect
from authentication.forms import UserEditForm
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from guardian.mixins import (
    LoginRequiredMixin
)

from marathon.models import SocialRequest
def index(request):
    '''
    redirects to profile detail view.
    '''
    profile = get_object_or_404(Profile, user__email=request.user.email)
    return redirect(profile, permanent=True)

class ProfileDetailView(LoginRequiredMixin, generic.detail.DetailView):
    model = Profile
    slug_field = 'user__email'
    slug_url_kwarg = 'email'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        request_profile = self.request.user.profile
        if not (self._is_owner() or self.object.is_friend(request_profile)):
            from recommander.models import Activity
            request_profile.activities.update_or_create(
                profile=self.object,
                activity_type=Activity.USER_VISITED
                )

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
        
    def get_context_data(self, **kwargs):
        kwargs.update({
            'owner': self._is_owner,
            'friends': self.object.contacts.all(),
            'are_friends': self.object.is_friend(self.request.user.profile),
            'just_logged_in': self.request.session['just_logged_in'],
            'is_request_sended': self.request.user.profile.marathon_sent.filter(to=self.object, label='friendship_request', status=SocialRequest.PENDING),
            'is_request_received': self.request.user.profile.marathon_received.filter(by=self.object, label='friendship_request', status=SocialRequest.PENDING),
            })
        self.request.session['just_logged_in'] = False
        return super(ProfileDetailView, self).get_context_data(**kwargs)

    def _is_owner(self):
        return self.request.user.email == self.kwargs.get('email')

class EditAccountView(LoginRequiredMixin, UserPassesTestMixin, generic.base.TemplateResponseMixin, generic.base.View):
    template_name = 'account/profile_update_form.html'
    success_url = 'account:profile_detail'
    user_keys = ['email', 'first_name', 'last_name']
    profile_keys = ['description']

    @classmethod
    def check_and_save_model_forms(cls, f1, f2):
        if f1.is_valid() and f2.is_valid():
            f1.save() and f2.save()
            return True
        return False

    def test_func(self):
      return self.request.user.email == self.kwargs.get('email')

    def post(self, request, *args, **kwargs):
        f1 = UserEditForm(self.request.POST, instance=request.user, editer=request.user)
        f2 = ProfileEditForm(self.request.POST, request.FILES, instance=request.user.profile)
        if not self.check_and_save_model_forms(f1, f2):
            self._handle_crispy_forms(f1, f2)
            return self.render_to_response({'f1': f1, 'f2': f2})

        messages.success(self.request, 'Account details updated', extra_tags='alert alert-success')
        return HttpResponseRedirect(reverse(self.success_url,
                                            args=[request.user.email]))

    def get(self, request, *args, **kwargs):
        f1 = UserEditForm(instance=request.user, editer=request.user)
        f2 = ProfileEditForm(instance=request.user.profile)

        self._handle_crispy_forms(f1, f2)
        return self.render_to_response({'f1': f1, 'f2': f2})

    def get_permission_object(self):
        obj = Profile.objects.get(user__email=self.kwargs.get('email'))
        return obj

    def _handle_crispy_forms(self, *forms):
        from crispy_forms.layout import Submit
        for form in forms:
            form.helper.form_tag = False
            form.helper.inputs.pop()


from django.core.paginator import Paginator
class NotificationsPaginator(Paginator):
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

from django.views.generic import ListView, TemplateView
from notifications.models import Notification

class UnreadedNotificationsListView(ListView):
  model = Notification
  template_name = 'account/notifications.html'
  paginate_by = 5
  paginator_class = NotificationsPaginator
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
    paginator_class = NotificationsPaginator
    paginate_by = 5
    # context_object_name = 'readed_notifications_list'

    @property
    def queryset(self):
        return Notification.objects.filter(recipient=self.request.user).read()

    def get_context_data(self, **kwargs):
        return super(ReadedNotificationsListView, self).get_context_data(
            unread=False,
            **kwargs
            )

