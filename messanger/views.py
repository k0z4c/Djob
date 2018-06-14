from django.shortcuts import render

from django.views.generic import (
    CreateView, ListView, FormView, DetailView
)

from .models import Message, Conversation
from .forms import MessageForm, ReplyForm

from django.urls import reverse 

from django.contrib import messages

from django.http import JsonResponse

from jsonview.decorators import json_view

class StartConversationView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messanger/message_form.html'

    @property
    def success_url(self):
        return reverse('messanger:conversations')

    def form_valid(self, form):

        recipient = form.cleaned_data['recipient']
        conversation = Conversation.objects.get_or_create_conversation(
            self.request.user.profile,
            profiles=[self.request.user._wrapped.profile, recipient.to]
        )
        self.object = form.save(commit=False)
        self.object.conversation = conversation
        self.object.sender = self.request.user.profile
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
        kwargs = super(StartConversationView, self).get_form_kwargs()
        kwargs.update({
                'profile': self.request.user.profile,
            })
        return kwargs

class ConversationReplyView(CreateView):
    model = Message
    form_class = ReplyForm

    @property
    def success_url(self):
        print(self.kwargs.get('pk'))
        return reverse('messanger:conversation_messages', args=[self.kwargs['pk'],])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        conversation = Conversation.objects.get(pk=self.kwargs['pk'])
        self.object.conversation = conversation
        self.object.save()

        conversation.last_message = self.object
        conversation.save()

        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(ConversationReplyView, self).get_form_kwargs()
        kwargs.update({
            'profile': self.request.user.profile,
            })
        return kwargs 

    def get_context_data(self, **kwargs):
        conversation = self.request.user.profile.conversation_set.get(pk=self.kwargs['pk'])
        context = {'last_message': conversation.last_message }
        return super().get_context_data(**context)

class ConversationListView(ListView):
    model = Conversation
    paginate_by = 5

    @property
    def queryset(self):
        return self.request.user.profile.conversation_set.all()

    def get_context_data(self, **kwargs):
        to_read = self.model.objects.get_conversations_to_read(self.request.user.profile)
        kwargs.update({'conversations_to_read': to_read})
        return super(ConversationListView, self).get_context_data(**kwargs)

class ConversationDetailView(DetailView):
    model = Conversation

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.read_messages(request.user)

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class ConversationMessagesListView(ListView):
    model = Message
    paginate_by = 5

    @property
    def queryset(self):
        try:
            self.kwargs['conversation'] = Conversation.objects.get(pk=self.kwargs['pk'])
        except Conversation.DoesNotExist:
            from django.http import HttpResponseNotFound
            return HttpResponseNotFound
        else:
            self.kwargs['conversation'].read_messages(self.request.user.profile)
            return self.kwargs['conversation'].messages.all()

    def get_context_data(self, **kwargs):
        context = {
        'conversation': self.kwargs['conversation'],
        'recipients': self.kwargs['conversation'].profiles.exclude(user__email=self.request.user.email)
        }
        return super().get_context_data(**context)


from jsonview.decorators import json_view
@json_view
def unread_count(request):
    unreaded_count = request.user.conversation_set.unread_messages_count(request.user)
    data = { 'unreaded_count': unreaded_count }
    return JsonResponse(data)



