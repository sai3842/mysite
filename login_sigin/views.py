from django.shortcuts import render,redirect
from django.shortcuts import redirect
from .models import usermodel
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password,check_password
from django.conf import settings
from .forms import usermodelform
import random
import time

# Create your views here.

def valadite(request):
            
            if request.method == 'POST':
                
               
                 otp= ''.join([
                      request.POST.get('otp1', ''),
                      request.POST.get('otp2', ''),
                      request.POST.get('otp3', ''),
                      request.POST.get('otp4', ''),
                      request.POST.get('otp5', ''),
                     request.POST.get('otp6', ''),
                 ])
                 try:
                      entered_otp= int(otp)
                 except:
                      return render(request, 'otp.html', {'msg': 'Invalid OTP format'})
                 
                 #otp_saved=request.session.get('otp')
                 otp_data=request.session.get('otp_data')
                 user_data = request.session.get('pending_user')


                # tme 2 min for otp
                 if time.time() - otp_data['created_at'] > 120:
                         del request.session['otp_data']  # remove expired OTP
                         return HttpResponse('OTP expired')
                 
                 
                 
                 #otp validation
                 if entered_otp == otp_data['otp'] :
                    user = usermodel(
                         username=user_data['username'],
                         email=user_data['email'],
                         password=user_data['password']
                        # you should hash this in real apps
                         )
                    user.save()

                    
                    del request.session['otp_data']  # remove OTP after use
                    del request.session['pending_user']
                  
                    return HttpResponse('saved')
                 else:
                     
                     return HttpResponse('not saved')
            return render(request,'otp.html')

              
def sig(request):
    if request.method == 'POST':
        uname=request.POST['username']
        mail=request.POST['email']
        pwd=request.POST['password']

        hash_pwd=make_password(pwd)
        
        
        request.session['pending_user']={
             'username': uname,
            'email': mail,
            'password': hash_pwd,
             
         }    

        
        if usermodel.objects.filter(username=uname).exists():
           
            return render(request,'sigup.html',{'data':'username already exists'})
        

         
        if usermodel.objects.filter(email=mail).exists():
            return render(request,'sigup.html',{'data':'email already exists'})
        

        
        dt=random.randint(10000,999999)
        #request.session['otp']=dt
        user_data=request.session['pending_user']

             
        semder_mail=user_data['email']

        subject = 'Your OTP Code '
        message = f'Your One-Time Password (OTP) is: {dt}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [semder_mail]
        request.session['otp_data'] = {
                 'otp': dt,
                  'created_at': time.time()  # store current time in seconds
                    }
        

        send_mail(subject, message, from_email, recipient_list)

        return redirect('otp')

          
        
             
    return render(request,'sigup.html',{'errors':'hi'})


def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password')

        user = usermodel.objects.filter(username=name).first()\
           or usermodel.objects.filter(email=name).first()

        if not user: 
                messages.error(request, "Invalid username or password")
                return render(request, "login.html")

        #user = authenticate(request, username=name, password=pwd)
        if check_password(pwd, user.password):
            request.session['user_id'] = user.id  # store user ID in session
            messages.success(request,name )
            request.session['user_name']=name
            print(name)
            return redirect('home')
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')

def forget(request):
     if request.method == 'POST':
          sender_mail=request.POST.get('email')

          if usermodel.objects.filter(email=sender_mail).exists():
               
                   #1,00,000  9,99,999
                   dt=random.randint(100000,999999)
          
                   subject='OTP FOR PASSWORD FORGET'
                   message=f'Your One-Time Password (OTP) is: {dt}'
                   from_email=settings.EMAIL_HOST_USER
                   recipient_list = [sender_mail]

                   request.session['email']={
                        'mail':sender_mail,
                   }

                   request.session['otp_data'] = {
                        'otp': dt,
                        'created_at': time.time()  # store current time in seconds
                    }
        

                   send_mail(subject,message,from_email,recipient_list)

                   return redirect('otp_forgrt_pwd')
          else:
               return render(request,'forgrt.html',{'data':'email not register'})
     return render(request,'forgrt.html')


def otp_forgrt_pwd(request):
            
            if request.method == 'POST':
                
               
                 otp= ''.join([
                      request.POST.get('otp1', ''),
                      request.POST.get('otp2', ''),
                      request.POST.get('otp3', ''),
                      request.POST.get('otp4', ''),
                      request.POST.get('otp5', ''),
                     request.POST.get('otp6', ''),
                 ])
                 try:
                      entered_otp= int(otp)
                 except:
                      return render(request, 'otp.html', {'msg': 'Invalid OTP format'})
                 
                 #otp_saved=request.session.get('otp')
                 otp_data=request.session.get('otp_data')
                 #user_data = request.session.get('pending_user')
                 otp_data['otp']


                # tme 2 min for otp
                 if time.time() - otp_data['created_at'] > 120:
                         del request.session['otp_data']  # remove expired OTP
                         return HttpResponse('OTP expired')
                 
                 
                 
                 #otp validation
                 if entered_otp == otp_data['otp'] :
           
                    return redirect('update_pwd')
                 else:
                     
                     return HttpResponse('not saved')
            return render(request,'otp.html')

def new_pwd(request):
     if request.method =='POST':
          new_password=request.POST.get('password')

          hash_new_password=make_password(new_password)
          mail_user=request.session['email']['mail']
          user=usermodel.objects.get(email=mail_user)
          user.password=hash_new_password
          user.save()

          del request.session['email']
          return render(request,'new_pwd.html',{'data':'Updated Sucessfully'})
     return render(request,'new_pwd.html')






   
   
  

          



              
       
    






