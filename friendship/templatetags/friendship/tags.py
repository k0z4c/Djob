from django import template
from django.template.defaulttags import register

register = template.Library()

@register.inclusion_tag('friendship/add_button.html')
def add_friend_button(user):
  return {'email': user.email}
