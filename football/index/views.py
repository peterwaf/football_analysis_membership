from django.shortcuts import render
from django.views import generic
from content.models import Post
from league.models import Leaguetype
#import paginator
from django.core.paginator import Paginator
from users.models import CustomUser
# Create your views here.

#default views for free content

def contentView(request):
    #filter only free content, content_type = 0
    posts = Post.objects.filter(status=1,content_type=0).order_by('-created_on')
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'posts':posts,'items':posts}

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
    
    paginator = Paginator(category_posts, 5)
    page = request.GET.get('page')
    category_posts = paginator.get_page(page)

    context = {'category_posts':category_posts,'single_league_category':single_league_category,'posts':posts,'items':category_posts}
    return render(request,"index/category_detail.html",context)

#default views for premium content with own templates

def premiumcontentView(request):
    #filter only paid content, content_type = 1
    premium_posts = Post.objects.filter(status=1,content_type=1).order_by('-created_on')
    paginator = Paginator(premium_posts,3)
    page = request.GET.get('page')
    premium_posts = paginator.get_page(page)
    context = {'premium_posts':premium_posts,'items':premium_posts}
    return render(request,"index/premium_index.html",context)

def premiumdetailedView(request,slug):
    singe_premium_post = Post.objects.get(slug=slug)
    #filter only paid content, content_type = 1
    premium_posts = Post.objects.filter(status=1,content_type=1).order_by('-created_on')
    context = {'singe_premium_post':singe_premium_post,'premium_posts':premium_posts}
    return render(request,"index/premium_inner_page.html",context)

def premiumcategorycontentView(request,league_id):
    #filter only paid content, content_type = 1 and league id
    premium_category_posts = Post.objects.filter(status=1,content_type=1,pk=league_id).order_by('-created_on')
    premium_posts = Post.objects.filter(status=1,content_type=1).order_by('-created_on')
    #initialise a single variable for each league category
    single_league_category = ''
    for league  in premium_category_posts:
        single_league_category = league.league

    paginator = Paginator(premium_category_posts, 3)
    page = request.GET.get('page')
    premium_category_posts = paginator.get_page(page)

    context = {'premium_category_posts':premium_category_posts,'single_league_category':single_league_category,'premium_posts':premium_posts,'items':premium_category_posts}
    return render(request,"index/premium_category_detail.html",context)