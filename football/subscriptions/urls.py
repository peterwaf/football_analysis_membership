"""my_bank URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from . import views
app_name = 'subscriptions'

urlpatterns = [
    path('subscribe/',views.subscribe,name='subscribe'),
    path('success/',views.subscription_success,name='success'),
    path('access/token/',views.getAccessToken,name='get_mpesa_access_token'),
    path('online/lipa/', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    path('callback/', views.callback, name='callback'),
    ]