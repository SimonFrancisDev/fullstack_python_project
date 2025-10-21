from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import SignUpForm, PostForm
from .models import User, Post, Follow, Message

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("feed")
    else:
        form = SignUpForm()
    return render(request, "core/signup.html", {"form": form})

@login_required
def feed(request):
    following_ids = Follow.objects.filter(follower=request.user).values_list("following_id", flat=True)
    posts = Post.objects.filter(author__id__in=list(following_ids) + [request.user.id])
    return render(request, "core/feed.html", {"posts": posts})

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("feed")
    else:
        form = PostForm()
    return render(request, "core/create_post.html", {"form": form})

@login_required
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user_profile)
    is_following = Follow.objects.filter(follower=request.user, following=user_profile).exists()
    followers_count = Follow.objects.filter(following=user_profile).count()
    following_count = Follow.objects.filter(follower=user_profile).count()
    context = {
        "user_profile": user_profile,
        "posts": posts,
        "is_following": is_following,
        "followers_count": followers_count,
        "following_count": following_count,
    }
    return render(request, "core/profile.html", context)

@login_required
def follow_toggle(request, username):
    if request.method == "POST":
        target = get_object_or_404(User, username=username)
        if target == request.user:
            return JsonResponse({"error": "cannot follow yourself"}, status=400)
        follow_obj, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            follow_obj.delete()
            state = "unfollowed"
        else:
            state = "followed"
        followers_count = Follow.objects.filter(following=target).count()
        return JsonResponse({"state": state, "followers_count": followers_count})
    return JsonResponse({"error": "POST required"}, status=400)

@login_required
def chat_room(request, username):
    other_user = get_object_or_404(User, username=username)
    return render(request, "core/chat.html", {"other_user": other_user})
