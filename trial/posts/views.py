from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

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
            Post.objects.create(
                author=request.user,
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text']
            )
            send_mail(
                f'new post from: {request.user.username}',
                'only on trial',
                'trial@example.com',
                ['to@example.com'],
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
    following = get_object_or_404(User, username=username)
    following_exists = Follow.objects.filter(
        follower=request.user,
        following=following
    ).exists()

    if request.user != following and not following_exists:
        Follow.objects.create(following=following, follower=request.user)
    return redirect('index')


@login_required
def unfollow(request, username):
    following = get_object_or_404(User, username=username)
    following_object = Follow.objects.filter(follower=request.user, following=following)
    if following_object.exists():
        following_object.delete()
        Post.objects.filter(author=following).update(read_status=False)
    return redirect('current_user_feed')


def current_user_feed(request):
    user_feed = Post.objects.select_related(
        'author'
    ).filter(
        author__following__in=Follow.objects.filter(follower=request.user)
    ).order_by('-pub_date')
    
    return render(request, 'current_user_feed.html', {
        'user_feed': user_feed
    })


def mark_as_read(request, post_id):
    read_mark = Post.objects.filter(id=post_id).update(read_status=True)
    return redirect('current_user_feed')