from django.shortcuts import render
from django.views import generic
from content.models import Post
from league.models import Leaguetype

# Create your views here.

def contentView(request):
    posts = Post.objects.filter(status=1).order_by('-created_on')
    categories = Leaguetype.objects.all()
    context = {'posts':posts,'categories':categories}
    return render(request,"index/index.html",context)


def detailedView(request,slug):
    singe_post = Post.objects.get(slug=slug)
    categories = Leaguetype.objects.all()
    context = {'singe_post':singe_post,'categories':categories}
    return render(request,"index/inner_page.html",context)

def categorycontentView(request,league_id):
    category_posts = Post.objects.filter(league_id=league_id).order_by('-created_on')
    #initialise a single variable for each league category
    single_league_category = ''
    for league  in category_posts:
        single_league_category = league.league
        
    categories = Leaguetype.objects.all()
    context = {'category_posts':category_posts,'categories':categories,'single_league_category':single_league_category}
    return render(request,"index/category_detail.html",context)
    

