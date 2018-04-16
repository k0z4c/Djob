from django.db import models
from django.utils import timezone 
from django.db import IntegrityError

from djob import settings 


class MessageManager(models.Manager):
    pass

class Conversation(models.Model):
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)

    is_broadcast = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_message_date = models.DateTimeField(auto_now=True)

class ReadQueue(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_read = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation)
    readed_by = models.ForeignKey(ReadQueue)

    creation_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=200)

    object = MessageManager()

    def __str__(self):
        return self.content

    # def read(self, user):
    #     if user not in self.conversation.members.all():
    #         raise IntegrityError

    #     self.readed_by.add(user=user)
    #     self.date_readed = timezone.now()


    #     if self.readed_by.filter().count() == self.conversation.members.filter().count():
    #         self.is_read = True
