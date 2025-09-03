from django.urls import path,include
from . import views

urlpatterns=[
   
    path('/',views.login_view,name='login'),
    path('/otp',views.valadite,name='otp'),
    path('/sigin',views.sig,name='sigin'),
   
    path('/forgrt',views.forget,name='forgrt'),
    path('/otp_forgrt_pwd',views.otp_forgrt_pwd,name='otp_forgrt_pwd'),
    path('/update_pwd',views.new_pwd,name='update_pwd')
   
    
]