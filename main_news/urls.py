from django.urls import path
from . import views


urlpatterns = [

    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('news/', views.main_page,name='news'),
    path('news/<slug:category_slug>/',views.main_page, name='news-category'),
    path('article/', views.article, name='article'),

]