from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	def serialize(self):
		return {
			"id": self.id,
			"username": self.username
		}

class User_followers(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_id")
	followers = models.ManyToManyField(User, related_name="following", blank=True)

	def __str__(self):
		return f"{self.user_id.username} has {self.followers.count()} followers"

	def serialize(self):
		return {
			"username": self.user_id.username,
			"followers": self.followers.count()
		}
		

class Post(models.Model):
	content = models.CharField(max_length=6400)
	user_p = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_p")
	likes = models.ManyToManyField(User, related_name="likes", blank=True)
	date_created = models.DateTimeField(auto_now=True)
	date_modified = models.DateTimeField(blank=True, null=True)
	is_modified = models.BooleanField(default=False)

	class Meta:
		ordering = ['-id']

	def __str__(self):
		return f"{self.id} {self.content} by {self.user_p.username}"

	def serialize(self):
		return {
			"id": self.id,
			"content": self.content,
            "user_p": self.user_p.username,
            "likes": self.likes.count(),
            "date_created": self.date_created.strftime("%b %-d %Y, %-I:%M %p"),
            "is_modified": self.is_modified
		}

class Likes(models.Model):
	is_liked = models.BooleanField(default=False)
	users = models.ManyToManyField(User, related_name="users")
	post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_id")