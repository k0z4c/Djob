
class PredictionEngine(object):
  def __init__(self, x, population, attrs, sample_misure=10):
    self.x = x
    self.attrs = attrs
    self.population = population
    self.sample_misure = sample_misure
    self.sample = self._sample(self.population, self.sample_misure)


  def _sample(self, population, sample_misure):
    import random
    if len(list(population)) < sample_misure:
      return population
    return random.sample(set(population), sample_misure)

  def predict(self):
    scores_list = ( self.fitness_score(self.x, y) for y in self.sample )
    results_list = list(map(lambda y: (y, next(scores_list)), self.sample))

    results_list.sort(key=lambda t: t[1], reverse=True)
    return ( r[0] for r in results_list )
  
  def fitness_score(self, x, y):
      score = 0
      for attr in self.attrs:
        if isinstance(attr, tuple):
          x_attr_set = set(( getattr(f, attr[1]) for f in getattr(x, attr[0]).all() ))
          y_attr_set = set(( getattr(f, attr[1]) for f in getattr(y, attr[0]).all() ))
        else:
          x_attr_set = set(getattr(x, attr).all())
          y_attr_set = set(getattr(y, attr).all())

        score += len(x_attr_set & y_attr_set)
      return score
