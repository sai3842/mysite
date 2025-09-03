from django.db import models

# Create your models here.

class orders(models.Model):
    ord_no=models.IntegerField(primary_key=True)
    u_name=models.CharField(max_length=100,null=False)
    amount=models.IntegerField()
    utr=models.IntegerField(null=True,blank=True)
    state=models.CharField(max_length=100,null=True)
