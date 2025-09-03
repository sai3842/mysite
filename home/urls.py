from django.shortcuts import render
from django.urls import path,include
from . import views

urlpatterns=[
    path('',views.homes,name='home'),
    path('h/',views.h),
    path('profile',views.prfile_view,name='profile')
]