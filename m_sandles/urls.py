from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.msandles,name='msandles'),
     path('<str:name>',views.msandles,name='mviews'),
   
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

