from rest_framework import generics, permissions
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer
from posts.models import Post
from core.permissions import IsCommentAuthorOrPostAuthorOrReadOnly, IsAuthenticatedOrReadOnly
from utils.notification_helpers import create_notification

# Create your views here.

class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id = self.kwargs['post_id'], parent_comment = None)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['post_id'])
        comment = serializer.save(user=self.request.user, post=post)
        create_notification(
            post.author,
            f"{self.request.user.username} commented on your post.",
            'comment',
            comment
        )
    

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsCommentAuthorOrPostAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CommentCreateSerializer
        return CommentSerializer


class ReplyListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(parent_comment_id = self.kwargs['comment_id'])
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        parent_comment = Comment.objects.get(pk=self.kwargs['comment_id'])
        serializer.save(user = self.request.user, post = parent_comment.post, parent_comment = parent_comment)