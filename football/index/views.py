from django.shortcuts import render,redirect
from django.views import generic
from django.db.models import Q
from content.models import Post
from league.models import Leaguetype
#import paginator
from django.core.paginator import Paginator
from users.models import CustomUser
#import django send mail module
from django.core.mail import send_mail
#import messages for forms
from django.contrib import messages
#import date time
from datetime import date, datetime, timedelta
#default views for free content
from django.contrib.auth import authenticate,login,logout

def contentView(request):
    #filter only free content, content_type = 0
    posts = Post.objects.filter(status=1,content_type=0).order_by('-created_on')
    league_lists = Leaguetype.objects.all()

    #querry function start

    query = request.GET.get('q')
    querrypremiumuser = request.GET.get('a')

    if query:
        #filter only free content by default when the user searches
        posts = Post.objects.filter(
            Q(title__icontains=query,status=1,content_type=0) | Q(content__icontains=query,status=1,content_type=0)
        ).distinct()
        league_lists = Leaguetype.objects.all() 
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        context = {'posts':posts,'items':posts,'league_lists':league_lists,'league_lists':league_lists}
        return render(request,"index/index.html",context)

    elif querrypremiumuser:
        #filter everything
        posts = Post.objects.filter(
            Q(title__icontains=query,status=1) | Q(content__icontains=query,status=1)
        ).distinct()
        league_lists = Leaguetype.objects.all() 
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        context = {'posts':posts,'items':posts,'league_lists':league_lists}
        return render(request,"index/index.html",context)

   #querry function end

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'posts':posts,'items':posts,'league_lists':league_lists}
    return render(request,"index/index.html",context)

def detailedView(request,slug):
    singe_post = Post.objects.get(slug=slug)
    league_lists = Leaguetype.objects.all()
    query = request.GET.get('q')
    querrypremiumuser = request.GET.get('a')

    if query:
        #filter only free content by default when the user searches
        posts = Post.objects.filter(
            Q(title__icontains=query,status=1,content_type=0) | Q(content__icontains=query,status=1,content_type=0)
        ).distinct()
        league_lists = Leaguetype.objects.all() 
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        context = {'posts':posts,'items':posts,'league_lists':league_lists,'league_lists':league_lists}
        return render(request,"index/index.html",context)

    elif querrypremiumuser:
        #filter everything
        posts = Post.objects.filter(
            Q(title__icontains=query,status=1) | Q(content__icontains=query,status=1)
        ).distinct()
        league_lists = Leaguetype.objects.all() 
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        context = {'posts':posts,'items':posts,'league_lists':league_lists,'league_lists':league_lists}
        return render(request,"index/index.html",context)

   #querry function end

    #filter only free content, content_type = 0
    posts = Post.objects.filter(status=1,content_type=0).order_by('-created_on')
    context = {'singe_post':singe_post,'posts':posts,'league_lists':league_lists}
    return render(request,"index/inner_page.html",context)
    
def categorycontentView(request,league_id):
    #filter only free content, content_type = 0 and league id
    category_posts = Post.objects.filter(status=1,content_type=0,league=league_id).order_by('-created_on')
    posts = Post.objects.filter(status=1,content_type=0).order_by('-created_on')
    league_lists = Leaguetype.objects.all()
    #initialise a single variable for each league category
    single_league_category = ''
    for league  in category_posts:
        single_league_category = league.league
    paginator = Paginator(category_posts, 5)
    page = request.GET.get('page')
    category_posts = paginator.get_page(page)
    query = request.GET.get('q')
    querrypremiumuser = request.GET.get('a')

    if query:
        #filter only free content by default when the user searches
        posts = Post.objects.filter(
            Q(title__icontains=query,status=1,content_type=0) | Q(content__icontains=query,status=1,content_type=0)
        ).distinct()
        league_lists = Leaguetype.objects.all() 
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        context = {'posts':posts,'items':posts,'league_lists':league_lists,'league_lists':league_lists}
        return render(request,"index/index.html",context)

    elif querrypremiumuser:
        #filter everything
        posts = Post.objects.filter(
            Q(title__icontains=query,status=1) | Q(content__icontains=query,status=1)
        ).distinct()
        league_lists = Leaguetype.objects.all() 
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        context = {'posts':posts,'items':posts,'league_lists':league_lists,'league_lists':league_lists}
        return render(request,"index/index.html",context)

   #querry function end


    context = {'category_posts':category_posts,
    'single_league_category':single_league_category,
    'posts':posts,'items':category_posts,
    'league_lists':league_lists}
    return render(request,"index/category_detail.html",context)

#default views for premium content with own templates

def premiumcontentView(request):
    #get the current user info from clicked session
    current_user = request.user
    if request.user.is_authenticated and current_user.subscription_end is None:
        return redirect('subscriptions:subscribe')
        #get the subscription end date of the current user
        current_user_subscription_end_date = current_user.subscription_end.date()
        #format the date variable
        date_format = "%Y-%m-%d"
        today = datetime.strptime(str(datetime.now().date()),date_format)
        #get the end date of the subscription of the user
        time_end_date = datetime.strptime(str(current_user_subscription_end_date),date_format)
        #get a difference
        time_diff = time_end_date - today
        #get the days only
        time_diff_days = time_diff.days
        #if the days are less than 1,then unsubscribe the user,set subscription dates to null and redirect them back to the page
        if time_diff_days < 1:
            current_user.subscribed = False
            current_user.subscription_start = None
            current_user.subscription_end = None
            current_user.save()
            return redirect('index:premium_tips')
    #filter only paid content, content_type = 1
    premium_posts = Post.objects.filter(status=1,content_type=1).order_by('-created_on')
    league_lists = Leaguetype.objects.all()
    query = request.GET.get('a')
    queryfree = request.GET.get('q')
    if query:
        #filter anything if the user is subscribed
        premium_posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
        league_lists = Leaguetype.objects.all()
        paginator = Paginator(premium_posts,3)
        page = request.GET.get('page')
        premium_posts = paginator.get_page(page)
        context = {'premium_posts':premium_posts,'items':premium_posts,'league_lists':league_lists}
        return render(request,"index/premium_index.html",context)

    elif queryfree:
         #filter FREE CONTENT if the user is unsubscribed # CONDITION CHECKED IN THE TEMPLATE
        premium_posts = Post.objects.filter(
            Q(title__icontains=queryfree,status=1,content_type=0) | Q(content__icontains=queryfree,status=1,content_type=0)
        ).distinct()
        league_lists = Leaguetype.objects.all()
        paginator = Paginator(premium_posts,3)
        page = request.GET.get('page')
        premium_posts = paginator.get_page(page)
        context = {'premium_posts':premium_posts,'items':premium_posts,'league_lists':league_lists}
        return render(request,"index/premium_index.html",context)
    
    paginator = Paginator(premium_posts,3)
    page = request.GET.get('page')
    premium_posts = paginator.get_page(page)
    context = {'premium_posts':premium_posts,
    'items':premium_posts,
    'league_lists':league_lists,
             }
    return render(request,"index/premium_index.html",context)

def premiumdetailedView(request,slug):
    singe_premium_post = Post.objects.get(slug=slug)
    league_lists = Leaguetype.objects.all()
    #filter only paid content, content_type = 1
    premium_posts = Post.objects.filter(status=1,content_type=1).order_by('-created_on')

    #querry function start

    query = request.GET.get('a')
    queryfree = request.GET.get('q')
    if query:
        #filter anything if the user is subscribed
        premium_posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
        league_lists = Leaguetype.objects.all()
        paginator = Paginator(premium_posts,3)
        page = request.GET.get('page')
        premium_posts = paginator.get_page(page)
        context = {'premium_posts':premium_posts,'items':premium_posts,'league_lists':league_lists}
        return render(request,"index/premium_index.html",context)

    elif queryfree:
         #filter FREE CONTENT if the user is unsubscribed # CONDITION CHECKED IN THE TEMPLATE
        premium_posts = Post.objects.filter(
            Q(title__icontains=queryfree,status=1,content_type=0) | Q(content__icontains=queryfree,status=1,content_type=0)
        ).distinct()
        league_lists = Leaguetype.objects.all()
        paginator = Paginator(premium_posts,3)
        page = request.GET.get('page')
        premium_posts = paginator.get_page(page)
        context = {'premium_posts':premium_posts,'items':premium_posts,'league_lists':league_lists}
        return render(request,"index/premium_index.html",context)

    #querry function end

    context = {'singe_premium_post':singe_premium_post,
    'premium_posts':premium_posts,
    'league_lists':league_lists,
    }
    return render(request,"index/premium_inner_page.html",context)

def premiumcategorycontentView(request,league_id):
    #filter only paid content, content_type = 1 and league id
    premium_category_posts = Post.objects.filter(status=1,content_type=1,league=league_id).order_by('-created_on')
    premium_posts = Post.objects.filter(status=1,content_type=1).order_by('-created_on')
    league_lists = Leaguetype.objects.all()
    #initialise a single variable for each league category
    single_league_category = ''
    for league  in premium_category_posts:
        single_league_category = league.league
    paginator = Paginator(premium_category_posts, 3)
    page = request.GET.get('page')
    premium_category_posts = paginator.get_page(page)

    #querry function start

    query = request.GET.get('a')
    queryfree = request.GET.get('q')
    if query:
        #filter anything if the user is subscribed
        premium_posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
        league_lists = Leaguetype.objects.all()
        paginator = Paginator(premium_posts,3)
        page = request.GET.get('page')
        premium_posts = paginator.get_page(page)
        context = {'premium_posts':premium_posts,'items':premium_posts,'league_lists':league_lists,'premium_category_posts':premium_category_posts,}
        return render(request,"index/premium_index.html",context)

    elif queryfree:
         #filter FREE CONTENT if the user is unsubscribed # CONDITION CHECKED IN THE TEMPLATE
        premium_posts = Post.objects.filter(
            Q(title__icontains=queryfree,status=1,content_type=0) | Q(content__icontains=queryfree,status=1,content_type=0)
        ).distinct()
        league_lists = Leaguetype.objects.all()
        paginator = Paginator(premium_posts,3)
        page = request.GET.get('page')
        premium_posts = paginator.get_page(page)
        context = {'premium_posts':premium_posts,'items':premium_posts,'league_lists':league_lists}
        return render(request,"index/premium_index.html",context)

    #querry function end
    
    context = {'premium_category_posts':premium_category_posts,
    'single_league_category':single_league_category,
    'premium_posts':premium_posts,
    'items':premium_category_posts,
    'league_lists':league_lists,
    }
    return render(request,"index/premium_category_detail.html",context)

#contact us

def contact_us(request):
    if request.method == "POST":
        form = request.POST
        name = form['txtName']
        email = form['txtEmail']
        phone = form['txtPhone']
        message = form['txtMsg']
        full_message = 'From : '+ name + '\n'+ 'Phone Number : ' + phone + '\n' + 'Message' + '\n' + message
        send_mail(
                'Customer Message from footballsuretips.com',
                full_message,
                email,
                ['peterwafula@gmail.com'],
                fail_silently=False,
            )
        return render(request,"index/message_sent.html")

    context = {}
    return render(request,"index/contact_us.html",context)


