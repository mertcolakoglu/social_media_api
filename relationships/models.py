from django.db import models
from django.conf import settings

# Create your models here.

class Relationship(models.Model):
    STATUS_CHOICES = [
        ('following', 'Following'),
        ('blocked', 'Blocked'),
    ]
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='relationships_from', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='relationships_to', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['from_user', 'to_user']


    def __str__(self):
        return f"{self.from_user.username} {self.status} {self.to_user.username}"