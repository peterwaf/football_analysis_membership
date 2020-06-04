from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from content.models import Post
from .forms import AddPosts
from django.utils import timezone

#update unicode
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
        if form.is_valid():
            Post = form.save(commit=False)
            Post.created_on = timezone.now()
            Post.author = request.user
            Post.save()
            messages.success(request,"Post Added successfully")
            return redirect('dashboard:add')
    else:
        form = AddPosts()
    context = {'form':form}
    return render(request,"dashboard/add_posts.html",context)

def editPost(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        form = AddPosts(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_on = timezone.now()
            post.author = request.user
            post.save()
            messages.success(request,"Post updated successfully")
            return render(request,"dashboard/success.html")
    else:
        form = AddPosts(instance=post)
    context = {'form':form}
    return render(request,"dashboard/add_posts.html",context)
    
    
