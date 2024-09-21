from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('my-posts/', views.UserPostListView.as_view(), name='user-post-list'),
    path('likes/', views.LikeListCreateView.as_view(), name='like-list-create'),
    path('likes/<int:pk>/', views.LikeDetailView.as_view(), name='like-detail'),
    path('likes/toggle/', views.LikeToggleView.as_view(), name='like-toggle'),
    path('hashtags/', views.HashtagListView.as_view(), name='hashtag-list'),
    path('hashtags/<int:pk>/', views.HashtagDetailView.as_view(), name='hashtag-detail'),
    path('posts-by-hashtag/', views.PostHashtagListView.as_view(), name='post-hashtag-list'),
    path('post-hashtags/<int:pk>/', views.PostHashtagDetailView.as_view(), name='post-hashtag-detail'),
]