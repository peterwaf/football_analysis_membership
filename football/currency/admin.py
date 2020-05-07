from django.contrib import admin

# Register your models here.
from .models import Currency

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('currency_code','currency_name')
    search_fields = ('currency_code','currency_name')


admin.site.register(Currency,CurrencyAdmin)