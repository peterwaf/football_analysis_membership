from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from content.models import Post
from .forms import AddPosts
from django.utils import timezone
from league.models import Leaguetype
from .forms import AddLeagues
from .forms import editUsers
from .forms import SubscriptionsForm
from users.models import CustomUser
from payments.models import Payments
from M_PESA.models import Mpesa
from subscriptions.models import Subscription

#update unicode
# Create your views here.
@login_required(login_url='users:login')
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
    return render(request,"dashboard/edit_posts.html",context)

#delete post
def deletePost(request,pk):
    current_post = Post.objects.get(pk=pk)
    current_post.delete()
    messages.success(request,"Post deleted successfully")
    return render(request,"dashboard/success.html")

#leagues

def allLeagues(request):
    all_leagues = Leaguetype.objects.all()
    template = "dashboard/all_leagues.html"
    context = {'all_leagues':all_leagues,
    }
    return render(request,template,context)

#add leagues

def addLeague(request):
    form = AddLeagues()
    if request.method == "POST":
        form = AddLeagues(request.POST)
        if form.is_valid():
            league = form
            league.save()
            messages.success(request,"League added successfully")
            return render(request,"dashboard/success.html")
        else:
            form = AddLeagues()
    context = {'form':form,
    }
    template = "dashboard/add_leagues.html"
    return render(request,template,context)

def editLeague(request,league_id):
    league = get_object_or_404(Leaguetype,pk=league_id)
    form = AddLeagues(instance=league)
    #if the form method is POST
    if request.method == "POST":
        #initialize the form variable with a filtered league instance object
        form = AddLeagues(request.POST,instance=league)
        #if the form is valid then save the data in the db
        if form.is_valid():
            leaguedb = form
            leaguedb.save()
            messages.success(request,"League edited successfully")
            return render(request,"dashboard/success.html")
        else:
            #if it is not valid then load it as an instance of the post
            form = AddLeagues(instance=league)
    context = {'form':form}
    template = "dashboard/edit_league.html"
    return render(request,template,context)

#users

#show all users

def allUsers(request):
    all_users = CustomUser.objects.all()
    template = "dashboard/all_users.html"
    context = { 'all_users':all_users,
    }
    return render(request,template,context)

#single user info

def userInfo(request,user_id):
    single_user = CustomUser.objects.get(pk=user_id)
    template = "dashboard/user_info_dashboard.html"
    context = { 'single_user':single_user,
    }
    return render(request,template,context)

def editUser(request,user_id):
    selected_user = get_object_or_404(CustomUser,pk=user_id)
    form = editUsers(instance=selected_user)
    #if form request method is post then load form instance object
    if request.method == "POST":
        form = editUsers(request.POST,instance=selected_user)
        if form.is_valid():
            form.save()
            messages.success(request,"User information updated successfully")
            return render(request,"dashboard/success.html")
        else:
            form = editUsers(instance=selected_user)
    template = "dashboard/edit_user.html"
    context = {'form':form}
    return render(request,template,context)

def customerPayments(request):
    all_payments = Payments.objects.all()
    template = "dashboard/payments.html"
    context = {'all_payments':all_payments}
    return render(request,template,context)

def mpesaData(request):
    mpesa_payments = Mpesa.objects.all()
    template = "dashboard/mpesa.html"
    context = {'mpesa_payments':mpesa_payments}
    return render(request,template,context)

def subscriptionsData(request):
    all_subsriptions = Subscription.objects.all()
    template = "dashboard/subscriptions.html"
    context = {'all_subsriptions':all_subsriptions}
    return render(request,template,context)

def editSubscriptions(request,subscription_id):
    selected_subscription = Subscription.objects.get(pk=subscription_id)
    form = SubscriptionsForm(instance=selected_subscription)
    if request.method == "POST":
        form = SubscriptionsForm(request.POST,instance=selected_subscription)
        if form.is_valid():
            subscription_data = form
            subscription_data.save()
            messages.success(request,"Subscription updated successfully")
            return render(request,"dashboard/success.html")
        else:
            form = SubscriptionsForm(instance=selected_subscription)
    template = "dashboard/edit_subscriptions.html"
    context = {'form':form}
    return render(request,template,context)

    
    
