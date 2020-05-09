from django.shortcuts import render,redirect
from .models import Subscription
from payments.models import Payments
#relative datetime installed from pip install django-relativedelta
from dateutil.relativedelta import relativedelta
#import python's datetime
from datetime import date,datetime
# Create your views here.
def subscribe(request):
    subscriptions = Subscription.objects.all()
    if request.method == "POST":
        form = request.POST
        user = request.user
        subscription = form['subscription']
        current_date = datetime.now()
        weekly_end_date = ''
        monthly_end_date = ''
        annual_end_date = ''
        amount = 0
        if subscription == "W":
            amount += 99
            weekly_end_date = current_date + relativedelta(weeks=1)
        elif subscription == "M":
            amount += 300
            monthly_end_date = current_date + relativedelta(months=1)
        elif subscription == "A":
            amount += 3000
            annual_end_date = current_date + relativedelta(years=1)
        else:
            amount += 0
    
    context = {'subscriptions':subscriptions}
    return render(request,"subscriptions/subscribeform.html",context)