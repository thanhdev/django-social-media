from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm, PostForm
from .models import Post


POSTS_PER_PAGE = 5


def get_posts_queryset():
    return (
        Post.objects.all()
        .select_related("user")
        .prefetch_related("liked_by")
        .annotate(likes_count=Count("liked_by"))
        .order_by("-created_at")
    )


@login_required(login_url="login")
def home(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect("home")
    else:
        form = PostForm()

    posts = get_posts_queryset()[:POSTS_PER_PAGE]

    return render(request, "home/index.html", {"posts": posts, "form": form})


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "home/register.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "home/login.html", {"form": form})


@login_required(login_url="login")
def get_posts(request):
    try:
        offset = int(request.GET.get("offset", 0))
    except ValueError:
        offset = 0
    posts = get_posts_queryset()[offset : offset + POSTS_PER_PAGE]
    return render(request, "home/components/post_list.html", {"posts": posts})


@login_required(login_url="login")
def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if post.user == request.user or request.user.is_superuser:
        post.delete()
    return redirect("home")


@login_required(login_url="login")
@require_POST
def like_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Post not found"}, status=404
        )

    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)
        liked = False
    else:
        post.liked_by.add(request.user)
        liked = True

    return JsonResponse(
        {
            "status": "success",
            "liked": liked,
            "likes_count": post.liked_by.count(),
        }
    )
