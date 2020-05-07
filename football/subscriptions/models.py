from django.db import models
from currency.models import Currency
# Create your models here.
SUBSCRIPTION_TYPE = (("W","Weekly"),
                     ("M","Monthly"),
                     ("A","Annually")
                    )

class Subscription(models.Model):
    subscription_type = models.CharField(max_length=10,choices=SUBSCRIPTION_TYPE,default=0)
    amount = models.FloatField()
    currency = models.ForeignKey(Currency,on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_subscriptions'
        
    def __str__(self):
        return self.subscription_type
    