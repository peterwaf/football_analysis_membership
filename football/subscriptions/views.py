from django.shortcuts import render,redirect
from .models import Subscription
# Create your views here.
def subscribe(request):
    subscriptions = Subscription.objects.all()
    context = {'subscriptions':subscriptions}
    return render(request,"subscriptions/subscribeform.html",context)