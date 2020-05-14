from django.contrib import admin
from .models import Payments
# Register your models here.
class PaymentsAdmin(admin.ModelAdmin):
    list_display =('user','start_date','end_date','subscription','amount','merchantId','validation')
    search_fields = ('subscription','amount','merchantId')

admin.site.register(Payments,PaymentsAdmin)