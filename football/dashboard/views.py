from django.shortcuts import render,redirect
from django.http import HttpResponse
from content.models import Post
from .forms import AddPosts
# Create your views here.
def dashboard(request):
    #show all posts
    all_posts = Post.objects.all()
    context = {'all_posts':all_posts}
    return render(request,"dashboard/dashboard.html",context)

def addPosts(request):
    form = AddPosts()
    if request.method == "POST":
        form = AddPosts(request.POST)
    else:
        form = AddPosts()
    context = {'form':form}
    return render(request,"dashboard/add_posts.html",context)