from django.shortcuts import render
from django.views.generic import TemplateView

class SuggestView(TemplateView):
    template_name = 'account/suggestions.html'

    def get(self, request, *args, **kwargs):
        import random
        import math
        user_profile = self.request.user.profile
        a_friend = random.choice(user_profile.contacts.all()).to
        print('friend selected {}'.format(a_friend.user.email))
        choices = math.ceil(len(user_profile.contacts.all())/4)
        profiles_sample = [ f.to for f in random.sample(set(a_friend.contacts.exclude(to=user_profile)), choices) ]
        print('random choices: {}'.format([p.user.email for p in profiles_sample ]))
        
        user_contacts_set = set(user_profile.contacts.all())
        user_projects_set = set(user_profile.projectpages.all())
        user_skilldata_set = set([ s.data for s in user_profile.skill_set.all()])

        profiles_scores_list = []
        for profile in profiles_sample:
            common_contacts = user_contacts_set & set(profile.contacts.all())
            common_projects = user_projects_set & set(profile.projectpages.all())
            common_skills = user_skilldata_set & set([ s.data for s in profile.skill_set.all()])
            profiles_scores_list.append(
                (profile.id, len(common_contacts | common_projects))
            )

        profiles_scores_list.sort(key=lambda t: t[1])
        print(profiles_scores_list)

        # dic = {}
        # for profile in profiles_sample:
        #     print('calculating fitness between {} {}'.format(user_profile.user.email, profile.user.email))
        #     dic.update({profile.id: self.calculate_fitness(user_profile, profile, attrs=['contacts', 'projectpages', 'skill_set'])})
        # print(dic)
        return super(SuggestView, self).get(request, *args, **kwargs)

    def calculate_fitness(self, a, b, attrs, filter=None):
        '''' filter is a callable that generates a list comprehnsion so a list, filtering data in sets or a tuple like (function, attr)'''
        score = 0
        for attr in attrs:
            a_attr_set = set(getattr(a, attr)).all()
            b_attr_set = set(getattr(b, attr)).all()
            score += len(a_attr_set & b_attr_set)

            print("{} {}".format(attr, score))
        return score

    def get_context_data(self, **kwargs):
        # kwargs.update({
        #     'profiles_suggested':
        #     })
        return super(SuggestView, self).get_context_data(**kwargs)    
