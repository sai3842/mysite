from django import forms
from django.contrib.auth.models import User

class usermodelform(forms.ModelForm):
    password=forms.CharField(max_length=20,widget=forms.PasswordInput)
    class Meta:
        model= User
        fields= ['username','email','password']
