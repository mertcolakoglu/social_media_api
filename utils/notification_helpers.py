from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification

def create_notification(user, content, notification_type, related_object):
    Notification.objects.create(
        user=user,
        content=content,
        notification_type=notification_type,
        content_type=ContentType.objects.get_for_model(related_object),
        object_id=related_object.id
    )