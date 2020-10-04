from django.contrib import admin

from .models import User, Post, User_followers, Likes
# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(User_followers)
admin.site.register(Likes)