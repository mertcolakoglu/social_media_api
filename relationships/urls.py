from django.urls import path
from . import views

urlpatterns = [
    path('relationships/', views.RelationshipListCreateView.as_view(), name='relationship-list-create'),
    path('relationships/<int:pk>/', views.RelationshipDetailView.as_view(), name='relationship-detail'),
    path('followers/', views.FollowersListView.as_view(), name='followers-list'),
    path('following/', views.FollowingListView.as_view(), name='following-list'),
]