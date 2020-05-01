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
            messages.success(request,'Account Successfuly Created ')
            context = {'form':form}
            return redirect('users:register')
        else:
            context = {'form':form}
    else:
        form = CreateUserForm()
        context = {'form':form}

    return render(request,"users/register.html",context)
    