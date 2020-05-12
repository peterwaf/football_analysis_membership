from django.shortcuts import render,redirect
from .models import Subscription
from payments.models import Payments
#relative datetime installed from pip install django-relativedelta
from dateutil.relativedelta import relativedelta
#import python's datetime
from datetime import date,datetime
#import custom user model
from users.models import CustomUser
import requests
from django.http import HttpResponse
import json #import JSON, which we help us to parse JSON string using json.loads()
from requests.auth import HTTPBasicAuth #HTTPBasicAuth from requests for authentication purpose.
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
# Create your views here.

def getAccessToken(request):
    consumer_key = '6jMNAQGooBZP0AXKPazEHTLXXq9eftyf'
    consumer_secret = 'A2i2xH5Jc6ZaR6YJ'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)

def lipa_na_mpesa_online(request,phone_number):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": phone_number,  # replace with customer phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": phone_number,  # replace with customer phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Football",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')

def subscription_success(request):
    context = {}
    return render(request,"subscriptions/subscription_success.html",context)

def subscribe(request):
    #get all subscriptions from the DB
    subscriptions = Subscription.objects.all()
    if request.method == "POST":
        form = request.POST
        subscription = form['subscription']
        phone_number = form['phone_number']
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
        lipa_na_mpesa_online(request,phone_number)
        #not sure how to validate if payment is made
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

