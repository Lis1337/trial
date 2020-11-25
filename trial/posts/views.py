from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Post, User
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


def user_profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    post = Post.objects.filter(author=user_profile)
    post_list = Post.objects.filter(author=user_profile).order_by('-pub_date').all()

    return render(request, 'user_profile.html', {
        'user_profile': user_profile,
        'post_list': post_list
    })


def follow(request):
    pass


def follow_list(request):
    pass


def unfollow(request):
    pass
