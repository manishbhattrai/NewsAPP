from django.contrib import admin
from .models import Post, Category,Like,Comment

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Comment)
