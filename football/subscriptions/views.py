from django.shortcuts import render,redirect
from .models import Subscription
from payments.models import Payments
#relative datetime installed from pip install django-relativedelta
from dateutil.relativedelta import relativedelta
#import python's datetime
from datetime import date,datetime
#import custom user model
from users.models import CustomUser
# Create your views here.
def subscribe(request):
    #get all subscriptions from the DB
    subscriptions = Subscription.objects.all()
    if request.method == "POST":
        form = request.POST
        subscription = form['subscription']
        #logged in user
        user = request.user
        #start date is the current instance of time
        start_date = datetime.now()
        #set default amount
        amount = 0
        #set end date to none before assignment
        end_date = None
        #grab current user subscription package from the DB
        user_subscription = Subscription.objects.get(pk=subscription)
        weekly_subscription = Subscription.objects.get(subscription_type="W")
        weekly_subscription_amount = weekly_subscription.amount
        monthly_subscription = Subscription.objects.get(subscription_type="M")
        monthly_subscription_amount = monthly_subscription.amount
        annual_subscription = Subscription.objects.get(subscription_type="A")
        annual_subscription_amount = annual_subscription.amount
        #if the choosen value is 1 from the form,set amount and global end date
        if subscription == "1":
            amount += weekly_subscription_amount
            end_date = start_date + relativedelta(weeks=1)
            print(end_date)
        elif subscription == "2":
            amount += monthly_subscription_amount
            end_date = start_date + relativedelta(months=1)
        elif subscription == "3":
            amount += annual_subscription_amount
            end_date = start_date + relativedelta(years=1)
        else:
            amount += 0
        #grab payments table and update with new values
        payments_data = Payments()
        payments_data.user = user
        payments_data.start_date = start_date
        payments_data.end_date = end_date
        payments_data.subscription = user_subscription
        payments_data.amount = amount
        payments_data.save()
        #change subscription of the user to True
        user.subscribed = True
        user.save()
        return redirect('subscriptions:success')
    context = {'subscriptions':subscriptions}
    return render(request,"subscriptions/subscribeform.html",context)


def subscription_success(request):
    context = {}
    return render(request,"subscriptions/subscription_success.html",context)