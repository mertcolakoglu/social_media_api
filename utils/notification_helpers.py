from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from django.utils import timezone
from datetime import timedelta

def create_notification(user, content, notification_type, related_object):
    Notification.objects.create(
        user=user,
        content=content,
        notification_type=notification_type,
        content_type=ContentType.objects.get_for_model(related_object),
        object_id=related_object.id
    )

def can_create_report(user, reported_object):
    from moderation.models import Report
    last_report = Report.objects.filter(
        reporter=user, 
        content_type=ContentType.objects.get_for_model(reported_object),
        object_id=reported_object.id,
        created_at__gte=timezone.now() - timedelta(days=1)
    ).first()
    return last_report is None