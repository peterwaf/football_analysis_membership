from django.shortcuts import render
from django.views import generic
from content.models import Post
from league.models import Leaguetype

# Create your views here.

def contentView(request):
    #show only free content
    free_posts = Post.objects.filter(status=1,content_type=0).order_by('-created_on')
    context = {'free_posts':free_posts}
    return render(request,"index/index.html",context)

def detailedView(request,slug):
    singe_post = Post.objects.get(slug=slug)
    free_posts = Post.objects.filter(status=1,content_type=0).order_by('-created_on')
    context = {'singe_post':singe_post,'free_posts':free_posts}
    return render(request,"index/inner_page.html",context)

def categorycontentView(request,league_id):
    category_posts = Post.objects.filter(status=1,content_type=0,pk=league_id).order_by('-created_on')
    free_posts = Post.objects.filter(status=1,content_type=0).order_by('-created_on')
    #initialise a single variable for each league category
    single_league_category = ''
    for league  in category_posts:
        single_league_category = league.league
    context = {'category_posts':category_posts,'single_league_category':single_league_category,'free_posts':free_posts}
    return render(request,"index/category_detail.html",context)



