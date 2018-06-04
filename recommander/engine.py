
class PredictionEngine(object):
  # contacts e projectpages sono modelli intermedi 
  # attrs = [('contacts', 'to'), 'projectpages', ('skill_set', 'data')]
  #                       -> attribute to access for intermediate model's instances 
  #  
  #  in kwargs we put this: list =
   #  if tuple:
  # ( getattr(f, 'to') for f in contacts.all())
  # ( getattr(s, 'data') for s in skill_set.all())
  # ( getattr(p, 'data') for p in project_pages.all())

  # ( f.to for f in contacts.all())
  # [(list of profiles friends), (list of projectpages instances), (list of ), ()]
  def __init__(self, x, population, attrs, sample_misure=10):
    '''
      inputs are profiles or qs?
    '''
    self.x = x
    self.attrs = attrs
    self.population = population
    self.sample_misure = sample_misure
    self.sample = self._sample(self.population, self.sample_misure)


  def _sample(self, population, sample_misure):
    import random
    if len(population) < sample_misure: 
      return population
    return random.sample(set(population), sample_misure)

  def predict(self):
    scores_list = ( self.fitness_score(self.x, y) for y in self.sample )
    results_list = list(map(lambda y: (y, next(scores_list)), self.sample))

    results_list.sort(key=lambda t: t[1], reverse=True)
    return ( r[0] for r in results_list )
  
  def fitness_score(self, x, y):
      '''
        returns the fitness score between x and y profiles on attrs.
        filter may be a callable for filtering on these attrs (skill_set data)
      '''
      score = 0
      for attr in self.attrs:
        if isinstance(attr, tuple):
          # we substitute the intermediate records with a select on a particular attribute (e.g. friendhip's intances)
          # this may be a good lambda girl
          x_attr_set = set(( getattr(f, attr[1]) for f in getattr(x, attr[0]).all() ))
          y_attr_set = set(( getattr(f, attr[1]) for f in getattr(y, attr[0]).all() ))
        else:
          # and this too
          x_attr_set = set(getattr(x, attr).all())
          y_attr_set = set(getattr(y, attr).all())

        score += len(x_attr_set & y_attr_set)
        # print('score: {} {} {}'.format(x, score, x_attr_set & y_attr_set))

      return score
