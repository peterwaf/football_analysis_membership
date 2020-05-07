from django.db import models

# Create your models here.
class Currency(models.Model):
    currency_code = models.CharField(max_length=100)
    currency_name = models.CharField(max_length=100)
    
    class Meta:
        
        db_table = 'tbl_currency'
        
    def __str__(self):
        return self.currency_code
    