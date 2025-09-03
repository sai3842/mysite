from django.contrib import admin
from .models import Product,Imageset,Size,Brand,Cate,Gender,Material,cart,coments
# Register your models here.

admin.site.register(Product)
admin.site.register(Imageset)
admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(Cate)
admin.site.register(Gender)
admin.site.register(Material)
admin.site.register(cart)
admin.site.register(coments)
