from django import template
from ...models import SocialRequest 
from django.template.defaulttags import register

register = template.Library()

# @register.inclusion_tag('marathon/request_counter.html')
# def counter(user, label):
#   notifications = Request.objects.filter(by=user, label=label)
#   context = {'unread_counter': notifications.count()}
#   return context
@register.inclusion_tag('marathon/request_list_pending.html', takes_context=True)
def socialrequest_received_pending_list(context, label):
  user = context.get('user', '')
  return {
    'requests': user.marathon_received.filter(label=label, status=SocialRequest.PENDING),
    'label': label
    }

@register.inclusion_tag('marathon/request_list_sent.html', takes_context=True)
def socialrequest_sent_list(context):
  user = context.get('user', '')
  return {
    'requests': user.marathon_sent.all(),
    }

@register.inclusion_tag('marathon/request_button.html')
def send_socialrequest_button(request_url):
  return {
    'request_url': request_url,
  }
