from django.shortcuts import render

from django.views.generic import (
    CreateView, ListView, FormView, DetailView
)

from .models import Message, Conversation
from .forms import MessageForm

from django.urls import reverse 

from django.contrib import messages

from django.http import JsonResponse

from jsonview.decorators import json_view


class CreateMessageView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messanger/message_form.html'

    @property
    def success_url(self):
        return reverse('account:profile_detail', args=(self.request.user,))

    def form_valid(self, form):

        recipient = form.cleaned_data['recipient']

        conversation = Conversation.objects.get_or_create_conversation(
            self.request.user,
            users=[self.request.user, recipient]
        )
        self.object = form.save(commit=False)
        self.object.conversation = conversation
        self.object.sender = self.request.user
        self.object.save()

        conversation.last_message = self.object
        conversation.save()

        messages.success(
            self.request,
            message='Message sent!',
            extra_tags='alert alert-success'
            )
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(CreateMessageView, self).get_form_kwargs()
        kwargs.update({
                'user': self.request.user,
            })
        return kwargs

class ConversationListView(ListView):
    model = Conversation

    @property
    def queryset(self):
        return self.request.user.conversation_set.all()

# when we see this we have read messages of this conversation
class ConversationDetailView(DetailView):
    model = Conversation

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()


        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

from jsonview.decorators import json_view
@json_view
def unread_count(request):
    unreaded_count = request.user.conversations.get_unread_messages(request.user).count()
    data = { 'unreaded_count': unreaded_count }
    return JsonResponse(data)



