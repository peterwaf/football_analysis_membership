from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Subscription
from payments.models import Payments
#relative datetime installed from pip install django-relativedelta
from dateutil.relativedelta import relativedelta
#import python's datetime
from datetime import date, datetime, timedelta
#import custom user model
from users.models import CustomUser
import requests
from django.http import HttpResponse
import json #import JSON, which we help us to parse JSON string using json.loads()
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth #HTTPBasicAuth from requests for authentication purpose.
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from M_PESA.models import Mpesa
import time
from django.db.models import Q

# Create your views here.
def lipa_na_mpesa_online(request,phone_number,amount):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,  # replace with customer phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": phone_number,  # replace with customer phone number to get stk push
        "CallBackURL": "http://5375c5640e41.ngrok.io/callback/", #already defined under urls,replace in production
        "AccountReference": phone_number,
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    json_data = json.loads(response.text)
    print('RESPONSE : ',json_data)

    if json_data.get('errorCode'): # check if we have and error from safcom
        """check if we have and error from safcom

        [DEV NOTES]: When getting an item from a dict use the 'json_data.get()' method instead of json_data[]
            as used in lines 45 and 59.
            This is prefred especially when the contents of the dict can change.
            Using .get() will not throw 'list out of index' errors.
        """
        return {
            'error': True,
            'errorCode': json_data.get('errorCode'),
            'errorMessage': json_data.get('errorMessage'),
        }

    return {
        'error': False,
        'merchant_request_id': json_data.get('MerchantRequestID')
    }



def getAccessToken(request):
    consumer_key = '6jMNAQGooBZP0AXKPazEHTLXXq9eftyf'
    consumer_secret = 'A2i2xH5Jc6ZaR6YJ'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)

def subscription_success(request):
    return render(request,"subscriptions/subscription_success.html")

def subscription_confirmation(request):
    """Renders a confirmation template
    This method checks if Safcom made a call to our callback.
    It check the merchant_id in the MPESA table
    """
    error_message = "Confirmation Error. Please click 'Confirm Payment' once again after few secconds or forward your MPESA message to 0722412676"
    if request.method == "POST":
        form = request.POST
        merchant_id = form.get('merchant_id')
        current_user = request.user

        if merchant_id:
            """This merchant_id is passed to template as context in line 92, 100, and 187.
            We query Mpesa table using the merchant_id and the last payment with the same merchant_id
            """
            mpesa_transaction = Mpesa.objects.filter(Q(merchant_id=merchant_id)&Q(result_code=0))
            payment = Payments.objects.filter(Q(merchantId=merchant_id)).last()
        else:
            """In case the merchant_id is not in the form. This is just a fallback incase the user decides to refresh the page
                or something that might cause the form to lose the merchant_id.
            1. We query the last payment this user made because we don't have the merchant_id. [Line 97]
            2. If we don't have records of this users' payment we show them an error msg [Line 99-102]
            3. If we have a record of payment we the proceed to query Mpesa table for payments that happened in the last 10 min. [Line 104-105]
                - Querying the last 10 min to avoid fetching payment user made a week ago or sometime in the past. (We can increase or reduce this time)
            4. Again if we don't have records of this users' payment we show them an error msg. [Line 107]
            5. Finally update Payments and user table and redirect to success page [Line 113-122]
            """
            payment = Payments.objects.filter(Q(user_id=current_user)).last()

            if not payment:
                messages.error(request, error_message)
                ctx = {'merchant_id': merchant_id}
                return render(request,"subscriptions/subscription_confirmation.html", ctx)

            ten_min_ago = datetime.now()-timedelta(minutes=10)
            mpesa_transaction = Mpesa.objects.filter(phone_number=payment.phone_number).filter(Q(created_at__gte=ten_min_ago)&Q(result_code=0))

        if not mpesa_transaction:
            messages.error(request, error_message)
            ctx = {'merchant_id': merchant_id}
            return render(request,"subscriptions/subscription_confirmation.html", ctx)

        payment.validation = True
        payment.save()

        start_date, end_date = get_subscription_period(payment.subscription.subscription_type)
        current_user.subscribed = True
        current_user.subscription_start = start_date
        current_user.subscription_end = end_date
        current_user.save()

        return redirect('subscriptions:success')

    return render(request, "subscriptions/subscription_confirmation.html")

"""
def format_phone_number(request,phone_number):
    if len(phone_number) < 9:
        messages.error(request,'Invalid phone number')
        return redirect('subscriptions:subscribe')
    else:
        return '254' + phone_number[-9:]
"""

def subscribe(request):
    #get all subscriptions from the DB
    subscriptions = Subscription.objects.all()
    if request.method == "POST":
        form = request.POST
        subscription = form['subscription']
        phone_number = form['phone_number']
        if len(phone_number) < 9:
            messages.error(request,'Invalid phone number')
            return redirect('subscriptions:subscribe')
        else:
            phone_number = '254' + phone_number[-9:]
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
        payment_request_response = lipa_na_mpesa_online(request,phone_number,amount)

        if payment_request_response['error']: # Handles when there was an error from safcom while making request
            messages.error(request, payment_request_response['errorMessage']) # TODO don't return error msg from safcom. Make the error msg more user friendly
            return redirect('subscriptions:subscribe')

        merchant_request_id = payment_request_response['merchant_request_id']

        #not sure how to validate if payment is made
        payments_data = Payments()
        payments_data.user = user
        payments_data.start_date = start_date
        payments_data.end_date = end_date
        payments_data.subscription = user_subscription
        payments_data.amount = amount
        payments_data.merchantId = merchant_request_id
        payments_data.phone_number = phone_number
        payments_data.validation = False
        payments_data.save()

        ctx = {'merchant_id': merchant_request_id}
        return render(request, "subscriptions/subscription_confirmation.html", ctx)

    context = {'subscriptions':subscriptions}
    return render(request,"subscriptions/subscribeform.html",context)


@csrf_exempt
def callback(request):
    json_data = json.loads(request.body)
    # print(json_data)
    body = json_data['Body']
    stkCallback = body['stkCallback']
    metadata = stkCallback.get('CallbackMetadata')
    print("\n Meta:",metadata)
    resultCode = stkCallback['ResultCode'] #to save in DB
    marchant_request_id = stkCallback['MerchantRequestID'] #to save in DB
    mpesa_database = Mpesa()
    if metadata:
        metadata_items = metadata.get('Item')
        transaction_code = metadata_items[1]
        transaction_phone_number_container = metadata_items[4]
        transaction_amount = metadata_items[0]
        mpesa_database.amount = transaction_amount['Value']
        mpesa_database.phone_number = transaction_phone_number_container['Value'] #to save in DB
        mpesa_database.transaction_code = transaction_code['Value'] #to save in DB
        mpesa_database.result_code = resultCode
        mpesa_database.merchant_id = marchant_request_id
        if resultCode == 0:
            #if transaction is valid, save
            mpesa_database.save()
        else:
            print('Callback Result code',resultCode)
    print('\nMerchantRequestID',' ',stkCallback['MerchantRequestID'])
    # query payments yable where mobile = 254723456789 and confirm=false
    data = {
        'status': 'ok'
    }
    return JsonResponse(data)

def get_subscription_period(subscription_type):
    """Generates start and end date of subscription
    """
    start_date = datetime.now()
    end_date = None
    if subscription_type == "W":
        end_date = start_date + relativedelta(weeks=1)
    elif subscription_type == "M":
        end_date = start_date + relativedelta(months=1)
    elif subscription_type == "A":
        end_date = start_date + relativedelta(years=1)
    return start_date, end_date
