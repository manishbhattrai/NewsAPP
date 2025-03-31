from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=50, null=False)
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('news-category', args=[self.slug])


    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.name)

            original_slug = self.slug

            count = 1

            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug} - {count}"

                count += 1
        
        super().save(*args, **kwargs)
    
    


    def __str__(self):
        return self.name
    

class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='post_categ', null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='news/')
    content = models.TextField()
    likes_count = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, through='Like', related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.title)

            original_slug = self.slug

            count = 1

            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug} - {count}"

                count += 1
        
        super().save(*args, **kwargs)
    
    def update_likes_count(self):
        self.likes_count = self.likes.count() 

        self.save()



    def __str__(self):
        return f"{self.author.username}'s Post."

class Like(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:

        unique_together = ('user', 'article')
    
    def __str__(self):
        return f"{self.user.username} liked {self.article.title}"  