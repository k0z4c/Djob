from django.db import models
from djob import settings 
from django.urls import reverse 
from django.db.models import Q
from django.utils import timezone

from django.core.serializers.json import DjangoJSONEncoder

from .managers import (
    ConversationManager,
)

from .fields import (
    DataJSONField, FormattedTextField,
)

class Conversation(models.Model):

    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    first_message = models.OneToOneField(
        'Message',
        related_name='first_message',
        null=True
        )
    last_message = models.OneToOneField(
        'Message',
        related_name='last_message',
        null=True
        )

    objects = ConversationManager()

    def get_absolute_url(self):
        return reverse('messanger:conversation_messages', args=(self.id,))

    def get_unread_messages(self, user):
        qs = ~Q(sender=user) & ~Q(read_at__has_key=user.email)
        return self.messages.filter(qs)

    def read_messages(self, user):
        qs = self.get_unread_messages(user)
        for mess in qs.filter(): 
            mess.read(user)

class GroupConversation(Conversation):
    '''
    Group concept is more specific than a Conversation.
    we have a title in a group conversation; it is handled 
    in a different manner; different maanger maybe also.
    future feature 
    '''
    pass

class Message(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        related_name='messages',
        null=True
    )
    sender = models.ForeignKey(settings.AUTH_USER_MODEL)

    read_at = DataJSONField(encoder=DjangoJSONEncoder, default=dict)
    message = FormattedTextField(max_length=200)
    _sent_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ['-_sent_at']

    @property
    def sent_at(self):
        from django.core.serializers.json import DjangoJSONEncoder
        return DjangoJSONEncoder().encode({'sent_at': self._sent_at})

    def read(self, user):
        self.read_at.update({user.email: timezone.now()})
        self.save()

    def is_read_by(self, user):
        return self.read_at.get(user.email, '')

    def last_user_read(self):
        return sorted(self.read_at, key=self.read_at.get, reverse=True)[0]

    def last_read(self):
        if not self.read_at:
            return DjangoJSONEncoder().encode({})
        import operator
        last_read = sorted(self.read_at.items(), key=operator.itemgetter(1), reverse=True)[0][1]
        return DjangoJSONEncoder().encode({'last_read': last_read})

    def __str__(self):
        return self.message[:100]

