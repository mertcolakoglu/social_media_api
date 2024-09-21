from rest_framework import serializers
from .models import Comment
from users.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    replies = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'parent_comment', 'content', 'created_at', 'updated_at', 'replies', 'replies_count']
        read_only_fields = ['user', 'post', 'parent_comment']
    
    def get_replies(self, obj):
        if obj.parent_comment is None:
            return CommentSerializer(obj.replies.all(), many = True).data
        return []
    
    def get_replies_count(self, obj):
        return obj.replies.count()
    

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']