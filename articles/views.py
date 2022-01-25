from django.shortcuts import render, redirect
from Blog.forms import postForm
from Blog.models import Post
# Create your views here.



def addPostPage(request):
    post = postForm()
    if request.method == 'POST':
        article_form = postForm(request.POST, request.FILES)
        if article_form.is_valid():
            instance = article_form.save(commit=False)
            instance.author=request.user
            instance.save()
            return redirect('/')
    context = {'post':post}
    return render(request, 'add_post.html', context)

def updatePage(request, pk):
    post = Post.objects.get(id=pk)
    article_form = postForm(instance=post)
    if request.method == 'POST':
        article_form = postForm(data=request.POST, instance=post)
        if article_form.is_valid():
            article_form.save()
            return redirect('home')
    context={'post':article_form}
    return render(request, 'update.html',context)

def deletePage(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('/')