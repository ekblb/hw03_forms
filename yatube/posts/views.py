from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .utils import paginator

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    posts = Post.objects.select_related('group', 'author').all()
    page_obj = paginator(posts, request)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('group', 'author').all()
    page_obj = paginator(posts, request)
    context = {
        'page_obj': page_obj,
        'group': group,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    author_posts = author.posts.select_related(
        'group', 'author').filter(author=author)
    page_obj = paginator(author_posts, request)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    author = post.author
    context = {
        'post': post,
        'author': author,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return render(request, 'posts:post_detail', post_id=post.id)
    form = PostForm(request.POST or None, instance=post)
    context = {
        'form': form,
    }
    if not form.is_valid():
        return render(request, 'posts/create_post.html', context)
    post = form.save()
    return redirect('posts:post_detail', post_id=post.id)
