from django.shortcuts import render,redirect,get_object_or_404
from .models import Category,Post,Like,Comment
from django.core.paginator import Paginator
from .forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):

    posts = Post.objects.order_by('-created_at').all() [:6]

    for post in posts:
        post.total_comments = post.comments.count()

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
    
    for post in posts:
        post.total_comments = post.comments.count()

    paginator = Paginator(posts,6)
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)

    context = {
        'pages': pages
    }

    return render(request,'news.html', context=context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def article(request,post_slug):

    user = request.user

    posts = get_object_or_404(Post, slug = post_slug)

    comments = posts.comments.all()

    total_comments = comments.count()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            comment = Comment(post=posts, user=user, content=content)
            comment.save()
            return redirect('article', post_slug=post_slug)
    
    else:
        form = CommentForm()

    context = {
        'posts':posts,
        'form':form,
        'comments':comments,
        'total_comments':total_comments,
    }

    return render(request,'article.html', context=context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def update_article(request, post_slug):

    post = get_object_or_404(Post, slug = post_slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():

          form.save()

          return redirect('dashboard')
    
    else:
        form = PostForm(instance=post)
    
    context = {
        'form':form,
        'post':post
    }
    
    return render(request, 'update_article.html', context=context)

@login_required(login_url='login')
def delete_article(request, post_slug):

    post = get_object_or_404(Post, slug = post_slug)

    post.delete()
    return redirect('dashboard')


@login_required(login_url='login')
def article_likes(request,post_slug):

    user = request.user

    posts = get_object_or_404(Post, slug = post_slug)

    existing_like = Like.objects.filter(user=user, article=posts).first()

    if existing_like:

        existing_like.delete()
    
    else:
        Like.objects.create(user=user, article=posts)

    
    posts.update_likes_count()


    return redirect('article',post_slug=post_slug)



