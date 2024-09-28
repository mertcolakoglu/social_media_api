from rest_framework import generics, permissions, serializers
from .models import Report
from .serializers import ReportSerializer, ReportUpdateSerializer
from utils.notification_helpers import create_notification, can_create_report
from django.contrib.auth import get_user_model
from core.permissions import IsAdminOrReporter

User = get_user_model()

class ReportListCreateView(generics.ListCreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Report.objects.all()
        return Report.objects.filter(reporter=self.request.user)

    def perform_create(self, serializer):
        reported_object = serializer.validated_data['reported_object']
        if can_create_report(self.request.user, reported_object):
            report = serializer.save(reporter=self.request.user)
            if hasattr(report.reported_object, 'author'):
                create_notification(
                    report.reported_object.author,
                    f"Your content has been reported by a user.",
                    'report',
                    report
                )
            for admin in User.objects.filter(is_staff=True):
                create_notification(
                    admin,
                    f"A new report has been filed by {self.request.user.username}.",
                    'report',
                    report
                )
        else:
            raise serializers.ValidationError("You've already reported this content in the last 24 hours.")

class ReportDetailView(generics.RetrieveUpdateAPIView):
    queryset = Report.objects.all()
    permission_classes = [IsAdminOrReporter]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ReportUpdateSerializer
        return ReportSerializer

    def perform_update(self, serializer):
        report = serializer.save()
        create_notification(
            report.reporter,
            f"The status of your report has been updated to {report.get_status_display()}.",
            'report_update',
            report
        )