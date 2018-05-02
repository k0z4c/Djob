from django.shortcuts import render

from jsonview.decorators import json_view
from django.views.generic import ListView
# Create your views here.

from .models import Request
from django.http import JsonResponse

@json_view
def unread_count(request):
  count = request.user.marathon_sended.filter().count()
  data = {
    'unread': count,
  }
  return JsonResponse(data)