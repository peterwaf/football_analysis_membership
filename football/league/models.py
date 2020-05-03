from django.db import models

# Create your models here.
class Leaguetype(models.Model):
    league = models.CharField(max_length=50)

class Meta:
        db_table = 'tbl_legue_type'

def __str__(self):
        return self.league