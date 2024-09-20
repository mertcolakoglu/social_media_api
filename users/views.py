from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer

# Create your views here.

class ProfileRetrieveUpdateApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile