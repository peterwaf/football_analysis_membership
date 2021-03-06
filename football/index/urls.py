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
app_name = 'index'

urlpatterns = [
    path('',views.contentView,name='home'),
    path('free-football-tips/',views.contentView,name='free_tips'),
    path('<slug:slug>/details', views.detailedView, name='post_detail'),
    path('<int:league_id>/free-tips',views.categorycontentView, name='category_detail'),
    path('premium-football-tips/',views.premiumcontentView,name='premium_tips'),
    path('<slug:slug>/premium-foootball-tips', views.premiumdetailedView, name='premium_post_detail'),
    path('<int:league_id>/premium-tips/',views.premiumcategorycontentView, name='premium_category_detail'),
    path('contact_us/',views.contact_us,name='contact_us'),

    
    
    ]

    