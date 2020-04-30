from django.shortcuts import render

# Create your views here.
def userRegistration(request):
    context = {}
    return render(request,"users/register.html",context)