from django.db import models

# Create your models here.

class country_wise(models.Model):
    name = models.CharField(max_length=50)
    total_cases =  models.IntegerField(null = True)
    total_des = models.IntegerField(null = True)
    cases_yesterday = models.IntegerField(null = True)
    des_yesterday = models.IntegerField(null = True)
    rec_yesterday = models.IntegerField(null = True)
    active_yesterday = models.IntegerField(null = True)
    country_code = models.CharField(max_length = 10, null = True)
    flag_url = models.CharField(max_length = 110, null = True)

    full_name = models.CharField(max_length = 110, null = True)
    

    def __str__(self):
        return self.name
    
