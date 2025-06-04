from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Category, Post, Reply
from .forms import PostForm, ReplyForm
from django.urls import reverse

# Create your views here.
def index(request):
    categories = Category.objects.annotate(
        post_count=Count('posts')
    ).order_by('name')

    recent_posts = Post.objects.select_related('author', 'category').order_by('-created_date')[:5]

    context = {
        'categories': categories,
        'recent_posts': recent_posts,
    }
    return render(request, 'forum/index.html', context)


def category_posts(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts_list = Post.objects.filter(category=category).select_related('author').annotate(
        reply_count=Count('replies')
    ).order_by('-is_pinned', '-created_date')

    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'forum/category_posts.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save(update_fields=['views'])
    replies = Reply.objects.filter(post=post, parent=None).select_related('author').prefetch_related(
        'children__author',
        'children__children__author',
        'children__children__children__author'
    ).order_by('created_date')

    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content', '').strip()
        parent_id = request.POST.get('parent_id')

        if content:
            reply = Reply(
                post=post,
                author=request.user,
                content=content
            )
            if parent_id:
                try:
                    parent_reply = Reply.objects.get(pk=int(parent_id), post=post)
                    reply.parent = parent_reply
                except (Reply.DoesNotExist, ValueError) as e:
                    reply.parent = None
            else:
                reply.parent = None

            reply.save()
            messages.success(request, 'Your reply has been posted!')

            return redirect(f"{reverse('forum:post_detail', kwargs={'pk': post.pk})}#reply-{reply.id}")

    reply_form = ReplyForm()

    context = {
        'post': post,
        'replies': replies,
        'reply_form': reply_form,
    }
    return render(request, 'forum/post_detail.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('forum:post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'forum/create_post.html', {'form': form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, 'You can only edit your own posts.')
        return redirect('forum:post_detail', pk=post.pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated!')
            return redirect('forum:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'forum/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, 'You can only delete your own posts.')
        return redirect('forum:post_detail', pk=post.pk)

    if request.method == 'POST':
        category_pk = post.category.pk
        post.delete()
        messages.success(request, 'Your post has been deleted!')
        return redirect('forum:category_posts', pk=category_pk)

    return render(request, 'forum/delete_post.html', {'post': post})