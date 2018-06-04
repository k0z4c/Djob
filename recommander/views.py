from django.shortcuts import render
from django.views.generic import TemplateView

from account.models import Profile
from .models import Activity
import random
class SuggestView(TemplateView):
    template_name = 'recommander/suggestions.html'

    def get(self, request, *args, **kwargs):
      # collect data; maybe in PredictionPredictionEngine?
      population = self._collect_data(self.request.user)
      # now instantce the engine for fitness computation over the sampling set
      from .engine import PredictionEngine
      attrs=[('contacts', 'to'), ('skill_set', 'data'), 'projectpages']
      engine = PredictionEngine(self.request.user.profile, population, attrs=attrs)
      self.profiles_suggested = [ profile for profile in engine.predict() ]
      print('suggested:', self.profiles_suggested)
      return super(SuggestView, self).get(request, *args, **kwargs)

    def _collect_data(self, user):
      user_profile = user.profile

      activities_profiles_visited = user_profile.activities.values_list('profile', flat=True)
      visited_profiles = Profile.objects.filter(pk__in=set(activities_profiles_visited))

      # print("visited = {}".format([s.user for s in visited_profiles]))
      def random_choice(qs):
        try:
          choice = random.choice(qs)
        except IndexError:
          choice = None
        return choice

      a_skill = random_choice(user_profile.skill_set.all())
      # print("skill selected {}".format(a_skill.data.codename))
      if a_skill:
        a_skill = a_skill.data
      skill_profiles = Profile.objects.filter(skill__data=a_skill).exclude(user=user)
      # print('skill profiles ={}'.format([ s.user for s in skill_profiles]))

      a_project = random_choice(user_profile.projectpages.all())
      project_profiles = Profile.objects.filter(projectpages=a_project).exclude(user=user)
      # print('project profiles ={}'.format([ s.user for s in project_profiles]))

      population_qs = visited_profiles.union(skill_profiles, project_profiles, visited_profiles)
      population_qs = population_qs.difference(Profile.objects.filter(contacts__to=user_profile))
      # print(population_qs)
      print('population: ', [ p.user.email for p in population_qs ])
      return population_qs

    def get_context_data(self, **kwargs):
        kwargs.update({
            'profiles_suggested': self.profiles_suggested
            })
        print(kwargs['profiles_suggested'])
        return super(SuggestView, self).get_context_data(**kwargs)    
