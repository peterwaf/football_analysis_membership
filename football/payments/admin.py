from django.contrib import admin
from .models import Payments
# Register your models here.
class PaymentsAdmin(admin.ModelAdmin):
    list_display =('user','start_date','end_date','subscription','amount','merchantId','validation','phone_number')
    search_fields = ('amount','merchantId','phone_number')
    list_filter = ('subscription','validation')

admin.site.register(Payments,PaymentsAdmin)