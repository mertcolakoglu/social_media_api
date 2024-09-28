from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'reporter', 'content_type', 'object_id', 'reason', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['reporter', 'status', 'created_at', 'updated_at']

class ReportUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['status']