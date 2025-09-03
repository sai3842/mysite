from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.wshoes,name='wshoes'),
    path('/<str:name>',views.wshoes,name='view'),
    
    
   
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

