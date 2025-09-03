from django.shortcuts import render
from django.http import HttpResponse
from login_sigin.models import usermodel

# Create your views here.

#def hom(request):
  #  return render(request,'home.html')

from django.urls import reverse

def homes(request):
    ns = request.session.get('user_name', None)

    if ns is None:
        user_nm = "Login"
        link = reverse('login')   # go to login
    else:
        user_nm = ns
        link = reverse('profile')  # go to profile

    return render(request, "main.html", {
        "msg": user_nm,
        "user_link": link
    })

def h(request):
    return render(request,'new.html')
def prfile_view(request):
    ns = request.session.get('user_name', None)
    user_data=usermodel.objects.get(username=ns)
    if ns is None:
        user_nm='Login'
    else:
        user_nm=ns


    return render(request,'profile.html',{'data':user_data,'username':user_nm})

