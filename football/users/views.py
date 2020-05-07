from django.shortcuts import render,redirect
#import user creation form
from .forms import CreateUserForm
#import messages from django
from django.contrib import messages
#import authenticate,login and logout
from django.contrib.auth import authenticate,login,logout

#import custom user
from .models import CustomUser

# Create your views here.

def userRegistration(request):
    context = {}
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account Successfuly Created, please login.')
            context = {'form':form}
            return redirect('users:register')
        else:
            context = {'form':form}
    else:
        form = CreateUserForm()
        context = {'form':form}

    return render(request,"users/register.html",context)

def userLogin(request):

    if request.method == "POST":
        form = request.POST
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('index:home')
        else:
            messages.info(request,'Invalid Email or Password,try gain')
            
    context = {}
    return render(request,"users/login.html",context)

#logout

def Logout(request):
    logout(request)
    return redirect('index:home')

#profile

def profile(request):
    context = {}
    return render(request,"users/profile.html",context)
    