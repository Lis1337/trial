from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Post, User
from .forms import PostForm


def index(request):
    return render(request, 'index.html')


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