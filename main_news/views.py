from django.shortcuts import render,redirect,get_object_or_404
from .models import Category,Post
from django.core.paginator import Paginator
from .forms import PostForm


# Create your views here.


def home(request):

    posts = Post.objects.order_by('-created_at').all() [:6]

    context = {
        'posts':posts
    }

    return render(request, 'home.html',context=context)

def main_page(request, category_slug=None):
    
    categories = None
    posts = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug = category_slug)
        posts = Post.objects.filter(category=categories).order_by('-created_at')
    
    else:
        posts = Post.objects.order_by('-created_at').all()

    paginator = Paginator(posts,6)
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)

    context = {
        'pages': pages
    }

    return render(request,'news.html', context=context)



def dashboard(request):

    user = request.user
    posts = Post.objects.filter(author=user).order_by('-created_at')
    post_count = posts.count()
    category_count = posts.values('category').distinct().count()

    paginator = Paginator(posts, 4)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    context = {
        'posts':page_obj,
        'post_count':post_count,
        'category_count': category_count,
    }

    return render(request, 'dashboard.html',context=context)



def article(request):

    return render(request,'article.html')

def add_article(request):

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        

        if form.is_valid():
            
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('/')
    
    else:
        form = PostForm()
    
    context ={
        'form':form
    }
    return render(request,'add_article.html',context=context)
