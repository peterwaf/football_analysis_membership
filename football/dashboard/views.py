from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
def dashboard(request):
    html = '<h1>This is a dashboard </h1>'
    return HttpResponse('html')