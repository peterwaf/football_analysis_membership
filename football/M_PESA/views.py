from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def mpesa(request):
    return HttpResponse('This works!')