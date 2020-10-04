
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("like/<int:post_id>", views.like, name="like"),
    path("tweet", views.tweet, name="tweet"),
    path("tweets", views.tweets, name="tweets"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/<str:username>/tweets", views.profile_tweets, name="profile_tweets"),
    path("profile/<str:username>/info", views.profile_info, name="profile_info"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("following_tweets", views.following_tweets, name="following_tweets"),
    path("following_tweets_load", views.following_tweets_load, name="following_tweets_load"),
    path("edit_tweet/<int:post_id>", views.edit_tweet, name="edit_tweet")
]
