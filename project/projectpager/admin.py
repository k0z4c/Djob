from django.contrib import admin
from .models import ProjectPage, Thread, Message

@admin.register(ProjectPage)
class ProjectPageAdmin(admin.ModelAdmin):
  pass

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
  pass

@admin.register(Message)
class ThreadAdmin(admin.ModelAdmin):
  pass