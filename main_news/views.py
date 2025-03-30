from django.shortcuts import render,redirect
from .models import Category,Post
from django.core.paginator import Paginator


# Create your views here.


def home(request):

    posts = Post.objects.order_by('-created_at').all() [:6]

    context = {
        'posts':posts
    }

    return render(request, 'home.html',context=context)

def main_page(request):

    posts = Post.objects.all()

    paginator = Paginator(posts,6)
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)

    context = {
        'pages': pages
    }

    return render(request,'news.html', context=context)



def dashboard(request):

    return render(request, 'dashboard.html')



def article(request):

    return render(request,'article.html')
