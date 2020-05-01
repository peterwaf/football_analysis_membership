#Import user creation form from django
from django.contrib.auth.forms import UserCreationForm
#import form class from django
from django import forms
#import CustomUser  model
from users.models import CustomUser

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(help_text="Email is required.")
    mobile_number = forms.CharField(help_text="Mobile number is required.")
    
    #meta class
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','mobile_number','email','password1','password2']
