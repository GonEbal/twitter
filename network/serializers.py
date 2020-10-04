from rest_framework import serializers

from .models import User, User_followers, Post, Likes

class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ['content', 'user_p']

	def validate_content(self, value):
		if len(value) > 240:
			raise serializers.ValidationError("This tweet is too long")
		return value

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username']