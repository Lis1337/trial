from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Post, User, Follow
from .forms import PostForm


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    return render(request, 'index.html', {'post_list': post_list})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            Post.models.create(
                author=request.user,
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text']
            )
            return redirect('index')
        return render(request, 'new_post.html', {'form': form})
    form = PostForm()
    return render(request, 'new_post.html', {'form': form})


def user_blog(request, username):
    user_blog = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user_blog).order_by('-pub_date').all()
    return render(request, 'user_blog.html', {
        'user_blog': user_blog,
        'post_list': post_list
    })


@login_required
def follow(request, username):
    follower = get_object_or_404(User, username=username)
    if follower != request.user:
        Follow.objects.get_or_create(following=request.user, follower=follower)
    return redirect('index', username=username)


@login_required
def unfollow(request, username):
    follower = get_object_or_404(User, username=username)
    following = Follow.objects.filter(follower=follower, following=request.user)
    if following.exists():
        following.delete()
    return redirect('index', username=username)


def follow_list(request):
    pass
