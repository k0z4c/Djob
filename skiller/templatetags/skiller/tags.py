from django import template
from django.template.defaulttags import register

register = template.Library()

@register.inclusion_tag('skiller/show_skills.html')
def list_skills(profile, n=None):
  return {
    'skills': profile.skill_set.filter()[:n] if n else profile.skill_set.all(),
    'profile': profile,
  } 