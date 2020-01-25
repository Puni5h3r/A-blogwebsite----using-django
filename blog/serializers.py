from rest_framework import serializers
from .models import Post,Comment

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title','content','status','slug')


class CommenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields =['email','name','body','created_on']


class PostDetailSerializer(serializers.ModelSerializer):
    comment = CommenSerializer()
    class Meta:
        model = Post
        fields = ('title', 'content', 'status', 'slug','comment')


