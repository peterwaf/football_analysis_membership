from django.db import models

# Create your models here.
class Mpesa(models.Model):
    phone_number = models.CharField(max_length=20)
    transaction_code = models.CharField(max_length=150)
    result_code = models.CharField(max_length=10)
    merchant_id = models.CharField(max_length=150)
    amount = models.FloatField()

    class Meta:
        db_table = 'tbl_mpesa'
        verbose_name_plural = 'MPesa'

    def __str__(self):
        return self.phone_number
        