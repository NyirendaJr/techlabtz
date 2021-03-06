from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse


def post_list(request):
    posts = Post.objects.exclude(published_date__isnull=True).order_by('-published_date')
    context = {
        'posts':posts,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/blog-post.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_draft_list')
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_draft_list')
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    user = request.user
    posts = Post.objects.all().filter(author=user).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_draft_list')


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:post_draft_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment = form.save(commit=False)
            comment.post = post
            comment.author = form.cleaned_data['author']
            comment.text = form.cleaned_data['text']
            comment.created_date = timezone.now()
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})



@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:post_detail', pk=comment.post.pk)

def author_details(request, pk):
    return HttpResponse(pk)
