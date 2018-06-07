from django import template
from django.template.defaulttags import register

register = template.Library()

@register.inclusion_tag('skiller/show_skills.html', takes_context=True)
def list_skills(context, profile, n=None):
  context.update({
    'skills': profile.skill_set.filter()[:n] if n else profile.skill_set.all(),    
  })
  return context
