from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import Post, Like, Hashtag, PostHashtag
from .serializers import PostSerializer, PostCreateSerializer, LikeSerializer, HashtagSerializer, PostHashtagSerializer
from core.permissions import IsAuthorOrReadOnly, IsPublicOrAuthor, IsAuthenticatedOrReadOnly
from utils.notification_helpers import create_notification

# Create your views here.

class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.annotate(likes_count = Count('likes'))
        if self.request.user.is_authenticated:
            return queryset.filter(is_public=True) | queryset.filter(author = self.request.user)
        return queryset.filter(is_public = True)


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer
        
    def perform_create(self, serializer):
        serializer.save (author = self.request.user)
    

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.annotate(likes_count = Count('likes'))
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    serializer_class = PostSerializer


class UserPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author = self.request.user).annotate(likes_count = Count('likes'))


class LikeListCreateView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeDetailView(generics.RetrieveDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]


class LikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        post_id = request.data.get('post_id')
        if not post_id:
            return Response({"error": "post_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            post = Post.objects.get (id = post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status = status.HTTP_404_NOT_FOUND)
        
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            create_notification(
                post.author,
                f"{request.user.username} liked your post.",
                'like',
                post
            )
            return Response({"status": "liked"}, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            return Response({"status": "unliked"}, status=status.HTTP_200_OK)

class HashtagListView(generics.ListAPIView):
    queryset = Hashtag.objects.annotate(posts_count=Count('posthashtag'))
    serializer_class = HashtagSerializer


class HashtagDetailView(generics.RetrieveAPIView):
    queryset = Hashtag.objects.annotate(posts_count=Count('posthashtag'))
    serializer_class = HashtagSerializer


class PostHashtagListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        hashtag_name = self.request.query_params.get('hashtag', None)
        queryset = Post.objects.annotate(likes_count = Count('likes'))
        if hashtag_name:
            return queryset.filter(posthashtag__hashtag__name=hashtag_name)
        return queryset


class PostHashtagDetailView(generics.RetrieveAPIView):
    queryset = PostHashtag.objects.all()
    serializer_class = PostHashtagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]