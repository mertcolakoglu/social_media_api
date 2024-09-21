from django.urls import path
from . import views

urlpatterns = [
    path('posts/<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    path('comments/<int:comment_id>/replies/', views.ReplyListCreateView.as_view(), name='reply-list-create'),
]