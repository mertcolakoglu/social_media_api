from rest_framework import serializers
from .models import Post, Like, Hashtag, PostHashtag
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    likes_count = serializers.IntegerField(read_only = True)
    hashtags = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'image', 'created_at', 'updated_at', 'is_public', 'likes_count', 'hashtags')
    
    def get_hashtags(self, obj):
        return obj.posthashtag_set.values_list('hashtag__name', flat=True)


class PostCreateSerializer(serializers.ModelSerializer):
    hashtags = serializers.ListField(child=serializers.CharField(), write_only=True, required = False)

    class Meta:
        model = Post
        fields = ('content', 'image', 'is_public', 'hashtags')
    

    def create(self, validated_data):
       hashtags_data = validated_data.pop('hashtags', [])
       post = Post.objects.create(**validated_data)

       for hashtag_name in hashtags_data:
           hashtag, _ = Hashtag.objects.get_or_create(name = hashtag_name)
           PostHashtag.objects.create(post = post, hashtag = hashtag)
        
       return post
    

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['user', 'post']


class HashtagSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Hashtag
        fields = ['id', 'name', 'created_at', 'posts_count']
    
    def get_posts_count(self, obj):
        return obj.posthashtag_set.count()


class PostHashtagSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField()
    hashtag = serializers.StringRelatedField()

    class Meta:
        model = PostHashtag
        fields = ['post', 'hashtag']