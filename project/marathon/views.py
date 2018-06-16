from django.shortcuts import render
from django.http import JsonResponse
from .models import SocialRequest
from jsonview.decorators import json_view

@json_view
def manage_request(request, pk):
  try:
    social_request = SocialRequest.objects.get(pk=pk)
  except SocialRequest.DoesNotExist:
    pass

  if request.POST['action'] == 'accept':
    social_request.accept()
  elif request.POST['action'] == 'reject':
    social_request.reject()

  return JsonResponse({})
