from django.contrib import admin
from .models import Subscription
# Register your models here.
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscription_type','amount','currency')
    search_fields = ('subscription_type',)

admin.site.register(Subscription,SubscriptionAdmin)