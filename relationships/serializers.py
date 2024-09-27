from rest_framework import serializers
from .models import Relationship
from users.serializers import UserSerializer

class RelationshipSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = Relationship
        fileds = ['id', 'from_user', 'to_user', 'status', 'created_at']
        read_only_fields = ['from_user']

class RelationshipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['to_user', 'status']