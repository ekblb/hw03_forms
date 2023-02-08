from django.core.paginator import Paginator
from django.shortcuts import (get_object_or_404,
                              render,
                              redirect)
from django.contrib.auth.decorators import login_required

from .models import Group, Post, User
from .forms import PostForm


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    author_posts = Post.objects.filter(author=author)
    author_post_count = author_posts.count()
    paginator = Paginator(author_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_profile = True
    context = {
        'author': author,
        'author_post_count': author_post_count,
        'page_obj': page_obj,
        'is_profile': is_profile,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    user_post_count = Post.objects.filter(id=post_id).count()
    context = {
        'post': post,
        'user_post_count': user_post_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    groups = Group.objects.all()
    context = {
        'form': form,
        'groups': groups,
    }
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user)
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = Post.objects.get(id=post_id)
    form = PostForm(request.POST or None, instance=post)
    context = {
        'form': form,
        'is_edit': is_edit,
        'post': post,
        'post_id': post_id,
    }
    if post.author == request.user:
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post_id=post.id)
        return render(request, 'posts/create_post.html', context)
    return render(request, 'posts:post_detail', post_id=post.id)
