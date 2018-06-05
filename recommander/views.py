from django.shortcuts import render
from django.views.generic import TemplateView

from account.models import Profile
from .models import Activity
from .engine import PredictionEngine
import random

class SuggestView(TemplateView):
    template_name = 'recommander/suggestions.html'

    def get(self, request, *args, **kwargs):
      population = self._collect_data(self.request.user)
      attrs=[('contacts', 'to'), ('skill_set', 'data'), 'projectpages']

      engine = PredictionEngine(self.request.user.profile, population, attrs=attrs)

      self.profiles_suggested = [ profile for profile in engine.predict() ]
      return super(SuggestView, self).get(request, *args, **kwargs)

    def _collect_data(self, user):
      user_profile = user.profile


      def random_choice(qs):
        try:
          choice = random.choice(qs)
        except IndexError:
          choice = None
        return choice

      # crawling profile data
      activities_profiles_visited = user_profile.activities.values_list('profile', flat=True)
      visited_profiles = Profile.objects.filter(pk__in=set(activities_profiles_visited))

      a_skill = random_choice(user_profile.skill_set.all())
      if a_skill: a_skill = a_skill.data
      skill_profiles = Profile.objects.filter(skill__data=a_skill).exclude(user=user)

      a_project = random_choice(user_profile.projectpages.all())
      project_profiles = Profile.objects.filter(
        projectpages=a_project, projectpages__isnull=False).exclude(user=user)

      # merging
      population_qs = Profile.objects.none().union(
        skill_profiles, project_profiles, visited_profiles
        )
      # filtering friends
      population_qs = population_qs.difference(Profile.objects.filter(contacts__to=user_profile))

      return population_qs

    def get_context_data(self, **kwargs):
        kwargs.update({
            'profiles_suggested': self.profiles_suggested
            })
        return super(SuggestView, self).get_context_data(**kwargs)    
