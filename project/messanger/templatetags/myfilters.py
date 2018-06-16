from django import template
from django.template.defaulttags import register

register = template.Library()

@register.filter
def get_item(dictionary ,key):
    return dictionary.get(key, '')

@register.simple_tag(takes_context=True)
def unread_messages_conversation_counter(context, conversation):
    user = context['request'].user
    count = conversation.get_unread_messages(user.profile).count()
    return count if count > 0 else ''