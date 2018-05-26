from django.db import models
from account.models import Profile

class ProjectPage(models.Model):
  profiles = models.ManyToManyField(
    Profile,
    related_name = 'projectpages')

  owner = models.ForeignKey(
    Profile,
    related_name='+')

  name = models.CharField(max_length=50)
  description = models.TextField()

  class Meta:
    permissions = (
      ('can_post_discussions', 'Can post new discussions to page.'),
      )
  def __str__(self):
    return self.name
