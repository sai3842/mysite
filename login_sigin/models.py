from django.db import models

# Create your models here.
class usermodel(models.Model):
    username=models.CharField(max_length=10,null=False,unique=True)
    email=models.EmailField(max_length=40,null=False,unique=True)
    password=models.CharField(max_length=130,null=False)
    
    def __str__(self):
        return self.username