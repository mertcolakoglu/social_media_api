from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Relationship
from .serializers import RelationshipSerializer, RelationshipCreateSerializer
from core.permissions import IsOwnerOrReadOnly

# Create your views here.

class RelationshipListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Relationship.objects.filter(from_user = self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RelationshipListCreateView
        return RelationshipSerializer
    
    def perform_create(self, serializer):
        serializer.save(from_user = self.request.user)
    

class RelationshipDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class FollowersListView(generics.ListAPIView):
    serializer_class = RelationshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Relationship.objects.filter(to_user = self.request.user, status = 'following')


class FollowingListView(generics.ListAPIView):
    serializer_class = RelationshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Relationship.objects.filter(from_user = self.request.user, status = 'following')
    
    