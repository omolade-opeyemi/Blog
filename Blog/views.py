from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import postForm, userAccount, CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def homePage(request):
    post = Post.objects.all().order_by('-date_created')
    context={'post':post}
    return render(request, 'index.html', context)

def contactPage(request):
    return render(request, 'contact.html')


def postPage(request, pk):
    post = Post.objects.get(id=pk)
    comments = post.comments.filter(active=True)
    stuff = get_object_or_404(Post, id=pk)
    total_likes = stuff.total_likes()
    liked = False
    if stuff.likes.filter(id=request.user.id).exists():
        liked = True
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('post', pk=post.id)
    else:
        comment_form=CommentForm()

    context = {'post':post, 'total_likes':total_likes, 'liked':liked,'comments':comments,'comment_form':comment_form,}
    return render(request, 'post.html', context)
    

def editProfile(request):
    user = request.user.Account
    if request.method == 'POST':
        form = userAccount(data=request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('profile')
    form = userAccount(instance=user)
    context = {'form':form}
    return render(request, 'edit.html', context)

def userPage(request, pk): 
    account = Account.objects.all()
    user = User.objects.get(id=pk)
    #post = Post.objects.filter(author=pk)
    #post1 = Post.objects.get(author=pk)
    p = user.post_set.all().order_by('-date_created')
    context={'post':p ,'user':user}
    return render(request, 'user.html', context)

def likePage(request, pk):
    post = get_object_or_404(Post, id=pk)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post', args=[str(post.id)]))



    #return redirect('post', pk=post.id)



