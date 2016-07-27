from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login


def persona_login(request):
    user = authenticate(assertion=request.POST['assertion'])

    if user:
        login(request, user)
    return HttpResponse('OK')
