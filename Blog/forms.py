from django.forms import ModelForm
from .models import *

class postForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['likes', 'author']

class userAccount(ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        exclude = ['user']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']