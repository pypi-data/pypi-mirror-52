import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

from .validators import validate_unsubscribe_link


User = get_user_model()


class Status(models.Model):
    SUBSCRIBE = 0
    UNSUBSCRIBE = 1
    STATUS_CHOICES = (
        (SUBSCRIBE, 'subscribe'),
        (UNSUBSCRIBE, 'unsubscribe'),
    )

    user = models.OneToOneField(User, models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=SUBSCRIBE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        verbose_name = 'status'
        verbose_name_plural = 'status'
        unique_together = (
            ('user', 'uuid'),
        )

    def __str__(self):
        return 'User {} - {}'.format(self.user_id, self.get_status_display())

    def subscribe(self):
        self.status = self.SUBSCRIBE
        self.save()

    def unsubscribe(self, refresh_uuid=True):
        self.status = self.UNSUBSCRIBE
        if refresh_uuid:
            self.uuid = uuid.uuid4()

        self.save()


class Notification(models.Model):
    FAIL = 0
    UNDONE = 1
    SUCCESS = 2
    STATUS_CHOICES = (
        (FAIL, 'fail'),
        (UNDONE, 'undone'),
        (SUCCESS, 'success'),
    )

    subject = models.CharField(max_length=255)
    message = models.TextField(validators=[validate_unsubscribe_link])
    html_message = models.TextField(
        null=True,
        blank=True,
        validators=[validate_unsubscribe_link],
    )
    create_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=UNDONE)
    finish_at = models.DateTimeField(null=True, blank=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.subject

    def finish(self):
        self.finish_at = now()
        self.save()

    def success(self):
        self.status = self.SUCCESS
        self.finish()

    def fail(self):
        self.status = self.FAIL
        self.finish()

    def save(self, **kwargs):
        self.full_clean()  # Call full clean to run validators
        super().save(**kwargs)
