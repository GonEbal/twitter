import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .serializers import PostSerializer
from django.core.paginator import Paginator

from .models import User, User_followers, Post, Likes


def index(request):
    tweets = Post.objects.all()
    user = request.user
    tweet_list = []
    for tweet in tweets:
        if user == tweet.user_p:
            serialized_tweet = tweet.serialize()
            serialized_tweet["editable"] = "yes"
            serialized_tweet["new_post"] = "no"
            tweet_list.append(serialized_tweet)
        else:
            serialized_tweet = tweet.serialize()
            serialized_tweet["editable"] = "no"
            serialized_tweet["new_post"] = "no"
            tweet_list.append(serialized_tweet)
    paginator = Paginator(tweet_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {'page_obj': page_obj})

#API for all tweets
def tweets(request):
    tweets = Post.objects.all()
    user = request.user
    tweet_list = []
    for tweet in tweets:
        if user == tweet.user_p:
            serialized_tweet = tweet.serialize()
            serialized_tweet["editable"] = "yes"
            serialized_tweet["new_post"] = "no"
            tweet_list.append(serialized_tweet)
        else:
            serialized_tweet = tweet.serialize()
            serialized_tweet["editable"] = "no"
            serialized_tweet["new_post"] = "no"
            tweet_list.append(serialized_tweet)
    return JsonResponse(tweet_list, safe=False)

#Get tweets of a certain user
def profile_tweets(request, username):
    user_profile = User.objects.get(username=username)
    tweets = Post.objects.filter(user_p=user_profile)
    user = request.user
    tweet_list = []
    for tweet in tweets:
        if user == tweet.user_p:
            serialized_tweet = tweet.serialize()
            serialized_tweet["editable"] = "yes"
            serialized_tweet["new_post"] = "no"
            tweet_list.append(serialized_tweet)
        else:
            serialized_tweet = tweet.serialize()
            serialized_tweet["editable"] = "no"
            serialized_tweet["new_post"] = "no"
            tweet_list.append(serialized_tweet)
    return JsonResponse(tweet_list, safe=False)

def following_tweets(request):
    return render(request, "network/following.html")

def following_tweets_load(request):
    user = request.user
    following = user.following.values_list("user_id__id", flat=True)
    tweet_list = []
    for x in following:
        el = (Post.objects.filter(user_p=x))
        elems = [tweet.serialize() for tweet in el]
        tweet_list.extend(elems)
    return JsonResponse(tweet_list, safe=False)

def profile_info(request, username):
    user = User.objects.get(username=username)
    try:
        user_info = User_followers.objects.get(user_id=user)
        #check = user.following.all()
        following = user.following.values_list("user_id__id", flat=True)
        posts_count = Post.objects.filter(user_p=user)
        #f_all = [x.user_id.username for x in check]
        #print (len(f_all))
    except User_followers.DoesNotExist:
        return JsonResponse({"error": "User doesnt have any followers."}, status=404)
    if request.user.username != username:
        if request.user in user_info.followers.all():
            return JsonResponse({"info":user_info.serialize(), "button": "Unfollow", "following": following.count(), "posts_count": posts_count.count()}, safe=False)
        else:
            return JsonResponse({"info":user_info.serialize(), "button": "Follow", "following": following.count(), "posts_count": posts_count.count()}, safe=False)
    else:
        return JsonResponse({"info":user_info.serialize(), "button": "Your profile", "following": following.count(), "posts_count": posts_count.count()}, safe=False)


def profile(request, username):
    user_profile = User.objects.get(username=username)
    tweets = Post.objects.filter(user_p=user_profile)
    user = request.user
    tweet_list = []
    for tweet in tweets:
        if user == tweet.user_p:
            serialized_tweet = tweet.serialize()
            serialized_tweet["editable"] = "yes"
            serialized_tweet["new_post"] = "no"
            tweet_list.append(serialized_tweet)
        else:
            serialized_tweet = tweet.serialize()
            serialized_tweet["editable"] = "no"
            serialized_tweet["new_post"] = "no"
            tweet_list.append(serialized_tweet)
    paginator = Paginator(tweet_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {'page_obj': tweet_list})

@csrf_exempt
def tweet(request, *args, **kwargs):
    pp = PostSerializer(request.POST or None)
    #print("Here is def_create",pp)
    print(request.body)
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    if data['content'] == "":
        return JsonResponse({
            "error": "Tweet cannot be empty."
        }, status=400)

    content = data.get("content")

    #serializer = PostSerializer(data=content or None)
    #print("serializer:", serializer)
    #if serializer.is_valid():
        #serializer.save()
        #print('Yes')

    new_tweet = Post(
        content=content,
        user_p=request.user
    )
    new_tweet.save()

    user = request.user
    if user == new_tweet.user_p:
        serialized_tweet = new_tweet.serialize()
        serialized_tweet["editable"] = "yes"
        serialized_tweet["new_post"] = "yes"
    else:
        serialized_tweet = new_tweet.serialize()
        serialized_tweet["editable"] = "no"
        serialized_tweet["new_post"] = "yes"
    return JsonResponse(serialized_tweet, safe=False)


@csrf_exempt
def like(request, post_id):
    # Query for requested email
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse({"error": f"{post}"}, status=404)

    # Update like's counter
    elif request.method == "POST":
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return JsonResponse(post.serialize(), safe=False)
        else:
            post.likes.add(request.user)
            return JsonResponse(post.serialize(), safe=False)
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or POST request required."
        }, status=400)

@csrf_exempt
def follow(request, username):
    # Query for requested email
    try:
        user_user = User.objects.get(username=username)
        user = User_followers.objects.get(user_id=user_user)
    except User_followers.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    if request.method == "GET":
        return JsonResponse({"error": f"{user}"}, status=404)

    elif request.method == "POST":
        if request.user.username != username:
            if request.user in user.followers.all():
                user.followers.remove(request.user)
                following = user_user.following.values_list("user_id__id", flat=True)
                #print(following.count())
                return JsonResponse({"info":user.serialize(), "button": "Follow", "following": following.count()}, safe=False)
            else:
                user.followers.add(request.user)
                following = user_user.following.values_list("user_id__id", flat=True)
                #print(following.count())
                return JsonResponse({"info":user.serialize(), "button": "Unfollow", "following": following.count()}, safe=False)
            return HttpResponse(status=204)
        else:
            following = user_user.following.values_list("user_id__id", flat=True)
            return JsonResponse({"info":user.serialize(), "button": "Your profile", "following": following.count()}, safe=False)

    # Follow must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or POST request required."
        }, status=400)

@csrf_exempt
def edit_tweet(request, post_id):
    if request.user == Post.objects.get(pk=post_id).user_p:
        if request.method == "POST":
            data = json.loads(request.body)
            content = data.get("edit_content")
            if data['edit_content'] == "":
                return JsonResponse({
                "error": "Tweet cannot be empty."
                }, status=400)
            else:
                Post.objects.filter(pk=post_id).update(content=content)
                return JsonResponse(Post.objects.get(pk=post_id).serialize(), status=200)
        else:
            return JsonResponse({
                "error": "POST request required."
            }, status=400)
    else:
        return JsonResponse({
                "error": "You dont have a access to this tweet"
            }, status=400)

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
            user_followers = User_followers(user_id=user)
            user_followers.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
