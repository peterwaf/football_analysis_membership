from django.contrib import admin
from .models import Mpesa
# Register your models here.
class MpesaAdmin(admin.ModelAdmin):
    list_display = ('phone_number','transaction_code','result_code','merchant_id')
    search_fields = ('phone_number','transaction_code')

admin.site.register(Mpesa,MpesaAdmin)