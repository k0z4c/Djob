from django.shortcuts import render
from django.http import JsonResponse
from .models import SocialRequest
from jsonview.decorators import json_view

@json_view
def manage_request(request, pk):
  print('is processing')
  print(request.POST)
  try:
    social_request = SocialRequest.objects.get(pk=pk)
  except SocialRequest.DoesNotExist:
    pass

  if request.POST['action'] == 'accept':
    print('is accepted')
    social_request.accept()
  elif request.POST['action'] == 'reject':
    social_request.reject()

  return JsonResponse({})
