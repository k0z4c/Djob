from django import template
from ...models import Request 
from django.template.defaulttags import register

register = template.Library()

@register.inclusion_tag('marathon/request_list.html')
def counter(user, label):
  notifications = Request.objects.filter(by=user, label=label)
  context = {'unread_counter': notifications.count()}
  return context
