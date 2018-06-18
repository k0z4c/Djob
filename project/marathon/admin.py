from django.contrib import admin
from .models import SocialRequest

@admin.register(SocialRequest)
class SocialRequestAdmin(admin.ModelAdmin):
  list_display = ('label', 'status', 'by', 'to', 'date', 'last_modified')

  def last_modified(self, obj):
    return obj.status_date
