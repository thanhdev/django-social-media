from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Q
from django.core.paginator import Paginator

from .forms import CustomUserCreationForm, PostForm
from .models import Post, PostComment, User

POSTS_PER_PAGE = 5


def get_posts_queryset():
    return (
        Post.objects.all()
        .select_related("user")
        .prefetch_related("liked_by")
        .prefetch_related("comments")
        .annotate(likes_count=Count("liked_by", distinct=True))
        .annotate(comments_count=Count("comments", distinct=True))
        .order_by("-created_at")
    )


@login_required
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


@login_required
def user_settings(request):
    if request.method == "POST":
        # Handle avatar upload
        if "avatar" in request.FILES:
            request.user.avatar = request.FILES["avatar"]

        # Update bio
        request.user.bio = request.POST.get("bio", "")

        request.user.save()
        messages.success(request, "Your settings were successfully updated!")
        return redirect("user_settings")

    return render(request, "home/settings.html")


@method_decorator(login_required, name="dispatch")
class CustomPasswordChangeView(PasswordChangeView):
    template_name = "home/password_change.html"
    success_url = reverse_lazy("password_change_done")


@login_required
def password_change_done(request):
    messages.success(request, "Your password was successfully updated!")
    return redirect("user_settings")


@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = get_posts_queryset().filter(user=user)
    context = {
        "profile_user": user,
        "posts": posts,
    }
    return render(request, "home/profile.html", context)


def search(request):
    query = request.GET.get("q")
    if query:
        users = (
            User.objects.filter(
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
            )
            .distinct()
            .order_by("-id")
        )
        posts = get_posts_queryset().filter(content__icontains=query)
    else:
        users = User.objects.none()
        posts = Post.objects.none()

    users_page = Paginator(users, 10).get_page(request.GET.get("users_page"))
    posts_page = Paginator(posts, 10).get_page(request.GET.get("posts_page"))

    context = {
        "query": query,
        "users": users_page,
        "posts": posts_page,
    }
    return render(request, "home/search_results.html", context)


@login_required
def get_posts(request):
    try:
        offset = int(request.GET.get("offset", 0))
    except ValueError:
        offset = 0
    posts = get_posts_queryset()[offset : offset + POSTS_PER_PAGE]
    return render(request, "home/components/post_list.html", {"posts": posts})


@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user or request.user.is_superuser:
        post.delete()
        return HttpResponse("", status=200)

    return HttpResponse("Unauthorized", status=403)


@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)

    post = get_object_or_404(get_posts_queryset(), id=post_id)

    return render(request, "home/components/post.html", {"post": post})


@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get("content")

    if not content:
        return HttpResponse("Comment content is required.", status=400)
    elif len(content) > 500:
        return HttpResponse("Comment content is too long.", status=400)

    PostComment.objects.create(user=request.user, post=post, content=content)
    post = get_object_or_404(get_posts_queryset(), id=post_id)

    return render(request, "home/components/post.html", {"post": post})


@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(PostComment, id=comment_id)
    post_id = comment.post_id

    if comment.user == request.user or request.user.is_superuser:
        comment.delete()

    post = get_object_or_404(get_posts_queryset(), id=post_id)
    return render(request, "home/components/post.html", {"post": post})
