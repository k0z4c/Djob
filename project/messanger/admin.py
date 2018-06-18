from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
  list_display = ['us1', 'us2', 'last_message' ]

  def us1(self, obj):
      return obj.profiles.first()

  def us2(self, obj):
    return obj.profiles.last()

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
  list_display = ['us2', 'us2', 'message' ]

  def us1(self, obj):
    return obj.conversation.profiles.first()

  def us2(self, obj):
    return obj.conversation.profiles.last()

