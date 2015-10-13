from django.conf import settings
from django.db import models
from django.utils import timezone

from django.contrib.contenttypes.models import ContentType

import jsonfield
from authentication.models import Account, Company
from .signals import event_logged

from swampdragon.models import SelfPublishModel
from messaging.dragon_serializers import EventLogSerializer


class Log(SelfPublishModel, models.Model):
    
    user = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        null=True,
        on_delete=models.SET_NULL
    )
    company = models.ForeignKey(Company, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    not_action = models.CharField(max_length=50, db_index=True)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    notification = models.BooleanField(default=False)
    viewed_by = models.ManyToManyField(Account, related_name='user_viewed', blank=True)
    extra = jsonfield.JSONField()
    serializer_class = EventLogSerializer

    @property
    def template_fragment_name(self):
        return "eventlog/{}.html".format(self.not_action.lower())

    class Meta:
        ordering = ["-timestamp"]


def log(user, company, not_action, notification, extra=None, obj=None):
    if (user is not None and not user.is_authenticated()):
        user = None
    if extra is None:
        extra = {}
    company = company
    content_type = None
    object_id = None
    if obj is not None:
        content_type = ContentType.objects.get_for_model(obj)
        object_id = obj.pk
    if notification is not None:
        notification = notification
    event = Log.objects.create(
        user=user,
        company=company,
        not_action=not_action,
        extra=extra,
        content_type=content_type,
        object_id=object_id,
        notification=notification
    )
    event_logged.send(sender=Log, event=event)
    return event
