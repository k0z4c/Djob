from django.db import models
from djob import settings 
from django.urls import reverse 
from django.db.models import Q
from django.utils import timezone

class ConversationManager(models.Manager):
    def get_or_create_conversation(self, user, users):
        for conversation in user.conversation_set.all():
            if conversation.users == users:
                return conversation

        conversation = self.create()
        conversation.users = users
        return conversation

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
        qs = self.messages.filter(read_at__has_key=user.email)
        return qs

class GroupConversation(Conversation):
    '''
    Group concept is more specific than a Conversation.
    we have a title in a group conversation; it is handled 
    in a different manner; different maanger maybe also
    '''
    pass

from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
# https://docs.djangoproject.com/en/1.11/topics/serialization/

class DataJSONField(JSONField):
    def deserialize_ecma262_datetime(self, value):
        # https://www.ecma-international.org/ecma-262/5.1/#sec-15.9.1.15
        # value = 'YYYY-MM-DDTHH:mm:ss.sss[Z|([+|-]HH:mm)]'
        value = value.replace(':', '')
        if value.endswith('Z'):
            value = value.replace('Z', '+0000')

        from datetime import datetime
        format_ecma262  = '%Y-%m-%dT%H%M%S.%f%z'
        return datetime.strptime(value, format_ecma262)

    def parse_datetime(self, value):
        value = { k: self.deserialize_ecma262_datetime(v) for k, v in value.items() }
        return value

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return self.parse_datetime(value)

class Message(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        related_name='messages',
        null=True
    )
    sender = models.ForeignKey(settings.AUTH_USER_MODEL)

    read_at = DataJSONField(encoder=DjangoJSONEncoder, default=dict)
    message = models.TextField(max_length=200)
    sent_at = models.DateTimeField(auto_now_add=True)
    # deleted_at = DataJSONField(ecoder=DjangoJSONEncoder, default=dict)

    def read(self, user):
        self.read_at.update({user.email: timezone.now()})

    def is_read_by(self, user):
        return self.read_at.get(user.email, '')

    # to remove
    def is_deleted_by_recipient(self):
        return bool(self.recipient_deleted_at)

    def __str__(self):
        return self.message[:100]

