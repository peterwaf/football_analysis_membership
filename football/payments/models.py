from django.db import models
from users.models import CustomUser
from subscriptions.models import Subscription
# Create your models here.

class Payments(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    subscription = models.ForeignKey(Subscription,on_delete=models.CASCADE)
    amount = models.FloatField()

    class Meta:
        db_table = 'tbl_payments'
    
    def __str__(self):
        return self.subscription

    