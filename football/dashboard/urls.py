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
app_name = 'dashboard'

urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('add_posts/',views.addPosts,name="add"),
    path('edit_post/<int:pk>/',views.editPost,name="edit_post"),
    path('all_leagues',views.allLeagues,name="all_leagues"),
    path('add_league',views.addLeague,name='add_league'),
    path('edit_league/<int:league_id>/',views.editLeague,name='edit_league'),
    path('all_users',views.allUsers,name='all_users'),
    path('user_info/<int:user_id>/',views.userInfo,name='user_info'),
    path('idit_user/<int:user_id>/',views.editUser,name='edit_user'),
    path('payments/',views.customerPayments,name='payments'),
    path('m-pesa/',views.mpesaData,name='mpesa'),
    path('subscriptions/',views.subscriptionsData,name='subscriptions'),
    path('edit_subscription/<int:subscription_id>/',views.editSubscriptions,name='edit_subscription'),

]