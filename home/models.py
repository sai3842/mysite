from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Gender(models.Model):
    name=models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name=models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.name

class Cate(models.Model):
    name=models.CharField(max_length=20,null=True)
  
    def __str__(self):
         return self.name

class Imageset(models.Model):
    img1=CloudinaryField('image')
    img2=CloudinaryField('image')
    img3=CloudinaryField('image')
    img4=CloudinaryField('image')

    def __str__(self):
        return f"imageset {self.id}"
    
class Material(models.Model):
    Material = models.CharField(max_length=30,null=True)
    Heel_type =  models.CharField(max_length=30,null=True)
    Water_resistance_level =  models.CharField(max_length=30,null=True)
    Sole_material =  models.CharField(max_length=30,null=True)
    Style =  models.CharField(max_length=30,null=True)
    Country_of_Origin =  models.CharField(max_length=30,null=True)

class Size(models.Model):
    size1=models.CharField(max_length=10,null=True)
    size2=models.CharField(max_length=10,null=True)
    size3=models.CharField(max_length=10,null=True)
    size4=models.CharField(max_length=10,null=True)
    size5=models.CharField(max_length=10,null=True)

    def __str__(self):
        return f"size {self.id}"
    
class Product(models.Model):
    name= models.CharField(max_length=30)
    prce= models.CharField(max_length=10)
    offer=models.CharField(max_length=10)
    about=models.CharField(max_length=30,null=True)

    inf1=models.CharField(max_length=50,null=True)
    inf2=models.CharField(max_length=50,null=True)
    inf3=models.CharField(max_length=50,null=True)
   
    # relations
    gender=models.ForeignKey(Gender,on_delete=models.CASCADE,related_name="products")
    cat=models.ForeignKey(Cate,on_delete=models.CASCADE,related_name="products")
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,related_name="products")
    image_set=models.OneToOneField(Imageset,on_delete=models.SET_NULL,null=True,blank=True)
    material=models.OneToOneField(Material,on_delete=models.SET_NULL,null=True,blank=True)
    size=models.OneToOneField(Size,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return f"{self.name} ({self.brand.name})"


class cart(models.Model):
    no=models.IntegerField(null=True,blank=True)
    user_name=models.CharField(max_length=30,null=True,blank=True)
    name=models.CharField(max_length=50)
    price=models.IntegerField()
    quantity=models.IntegerField()
    size = models.CharField(max_length=20, null=True, blank=True)
    image=CloudinaryField('image')

    def __str__(self):
        return self.name

class coments(models.Model):
    no=models.IntegerField()
    user_name=models.CharField(max_length=20,null=False)
    user_com=models.CharField(max_length=200)

    def __str__(self):
        return self.user_name
