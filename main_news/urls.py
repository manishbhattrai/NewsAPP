from django.urls import path
from . import views


urlpatterns = [

    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('news/', views.main_page,name='news'),
    path('news/<slug:category_slug>/',views.main_page, name='news-category'),
    path('article/<slug:post_slug>/', views.article, name='article'),
    path('add-article/', views.add_article, name='add_article'),
    path('update-article/<slug:post_slug>/', views.update_article, name='update_article'),
    path('delete-article/<slug:post_slug>/', views.delete_article, name='delete_article'),
    path('article/<slug:post_slug>/like/', views.article_likes, name='article_likes'),


]