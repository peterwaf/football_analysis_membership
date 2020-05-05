from django.shortcuts import render
from django.views import generic
from content.models import Post
from league.models import Leaguetype

# Create your views here.

#default views for free content

def contentView(request):
    #filter only free content, content_type = 0
    posts = Post.objects.filter(status=1,content_type=0).order_by('-created_on')
    context = {'posts':posts}
    return render(request,"index/index.html",context)

def detailedView(request,slug):
    singe_post = Post.objects.get(slug=slug)
    #filter only free content, content_type = 0
    posts = Post.objects.filter(status=1,content_type=0).order_by('-created_on')
    context = {'singe_post':singe_post,'posts':posts}
    return render(request,"index/inner_page.html",context)

def categorycontentView(request,league_id):
    #filter only free content, content_type = 0 and league id
    category_posts = Post.objects.filter(status=1,content_type=0,pk=league_id).order_by('-created_on')
    posts = Post.objects.filter(status=1,content_type=0).order_by('-created_on')
    #initialise a single variable for each league category
    single_league_category = ''
    for league  in category_posts:
        single_league_category = league.league
    context = {'category_posts':category_posts,'single_league_category':single_league_category,'posts':posts}
    return render(request,"index/category_detail.html",context)

#default views for premium content

def premiumcontentView(request):
    #filter only paid content, content_type = 1
    posts = Post.objects.filter(status=1,content_type=1).order_by('-created_on')
    context = {'posts':posts}
    return render(request,"index/premium_index.html",context)

def premiumdetailedView(request,slug):
    singe_post = Post.objects.get(slug=slug)
    #filter only paid content, content_type = 1
    posts = Post.objects.filter(status=1,content_type=1).order_by('-created_on')
    context = {'singe_post':singe_post,'posts':posts}
    return render(request,"index/premium_inner_page.html",context)

def premiumategorycontentView(request,league_id2):
    #filter only paid content, content_type = 1
    category_posts = Post.objects.filter(status=1,content_type=1,pk=league_id2).order_by('-created_on')
    posts = Post.objects.filter(status=1,content_type=1,pk=league_id2).order_by('-created_on')
    #initialise a single variable for each league category
    single_league_category = ''
    for league  in category_posts:
        single_league_category = league.league
    context = {'category_posts':category_posts,'single_league_category':single_league_category,'posts':posts}
    return render(request,"index/premium_category_detail.html",context)