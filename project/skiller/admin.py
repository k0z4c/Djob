from django.contrib import admin
from .models import Skill, SkillData

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
  list_display = ['profile', 'skilldata']

  def skilldata(self, obj):
    return obj.data

@admin.register(SkillData)
class SkillDataAdmin(admin.ModelAdmin):
  pass

