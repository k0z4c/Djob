from django import template
from django.template.defaulttags import register

register = template.Library()

@register.inclusion_tag('list_messages.html', takes_context=True)
def list_messages(context):
  return { 'messages': context.get('messages', None) }