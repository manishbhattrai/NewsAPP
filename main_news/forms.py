from django import forms
from .models import Post, Category, Comment



class PostForm(forms.ModelForm):

    category = forms.ModelChoiceField(
               queryset=Category.objects.all(),
               required=True
            )
    
    class Meta:
        model = Post
        fields = ['title','category','image','content']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']

