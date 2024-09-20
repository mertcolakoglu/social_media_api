from django.urls import path
from .views import ProfileRetrieveUpdateApiView

urlpatterns = [
    path('me/', ProfileRetrieveUpdateApiView.as_view(), name='profile-detail')
]
