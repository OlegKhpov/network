import json

from django.contrib.auth import authenticate, login, logout
from django.core import paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import Follower, Post, User, Like


def index(request):
    posts = Post.objects.order_by("-creation_date").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html', {'page_obj': page_obj})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def followed_posts(request):
    filtered, created = Follower.objects.get_or_create(
        owner=request.user
    )
    
    posts = Post.objects.filter(author__in=[fol for fol in filtered.followers.all()]).order_by("-creation_date").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/followed.html', {'page_obj': page_obj})


def profile(request, id):
    user_page = get_object_or_404(
        klass=User,
        id=id,
    )
    follow_button = False
    if user_page in [f for f in Follower.objects.get(owner=request.user).followers.all()]:
        follow_button = True
    followed, created = Follower.objects.get_or_create(owner=user_page)
    followers = [f for f in Follower.objects.all() if user_page in f.followers.all()]
    return render(request, 'network/profile.html', {
        'user_page': user_page,
        'followed': followed.followers.all(),
        'person_followers': followers,
        'followers_count': len(followers),
        'posts': Post.objects.filter(author=user_page),
        'follow_button': follow_button
    })


# JS utilites
@csrf_exempt
@login_required
def toggle_like(request, id):
    post = Post.objects.get(id=id)
    user = request.user
    like, created = Like.objects.get_or_create(
        post=post,
        user=user,
    )
    if created:
        return JsonResponse({'message': True})
    else:
        like.delete()
        return JsonResponse({'message': False})


@csrf_exempt
def edit(request, id):
    if request.method != "POST":
            return JsonResponse({"error": "POST request required."}, status=400)
    post = Post.objects.get(id=id)
    data = json.loads(request.body)
    text = data.get('text', '')
    header = data.get('header', '')
    if text == ['']:
        return JsonResponse({'error': "Text must not be empty!"})
    if header == ['']:
        return JsonResponse({'error': "Header must not be empty!"})
    post.header = header
    post.text = text
    post.save()
    return JsonResponse({'message': "Post created and posted."})


@csrf_exempt
@login_required
def make_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    text = data.get('text', '')
    header = data.get('header', '')
    if text == ['']:
        return JsonResponse({'error': "Text must not be empty!"})
    if header == ['']:
        return JsonResponse({'error': "Header must not be empty!"})
    post = Post(
        author=request.user,
        text=text,
        header=header,
    )
    post.save()
    return JsonResponse({'message': "Post created and posted."})


@login_required
def toggle_follow(request, id):
    user = request.user
    person_to_follow = get_object_or_404(
        klass=User,
        id=id,
        )
    follow = Follower.objects.get(
        owner=user,
    )
    if person_to_follow in follow.followers.all():
        follow.unfollow(user, person_to_follow)
        return JsonResponse({'message': False})
    follow.follow(user, person_to_follow)
    return JsonResponse({'message': True})


def get_like_info(request, id):
    if Like.objects.filter(post=id, user=request.user).count():
        return JsonResponse({'result': True})
    return JsonResponse({'result': False})
