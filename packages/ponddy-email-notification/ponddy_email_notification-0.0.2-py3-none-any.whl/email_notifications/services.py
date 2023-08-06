import logging

from django.core.mail import EmailMultiAlternatives, get_connection
from django.conf import settings
from django.db.models import Q
from django.http.request import HttpRequest
from django.template import Template, Context
from django.urls import reverse_lazy


from .models import Notification, Status


logger = logging.getLogger('django')
from_email = getattr(settings, 'EMAIL_HOST_USER')
unsubscribe_url = getattr(settings, 'unsubscribe_url', 'unsubscribe')


def send_notification(request: HttpRequest, instance: Notification):
    users = list(
        instance.users
        .select_related('status')
        .filter(Q(status__status=Status.SUBSCRIBE) | Q(status__status=None))
        .exclude(Q(email__isnull=True) | Q(email__exact='')),
    )

    # Update user list, only save user that have been send.
    instance.users.clear()
    instance.users.add(*users)

    if not users:
        instance.success()
        return

    # Create status for no status users
    Status.objects.bulk_create([
        Status(user=user) for user in
        filter(lambda u: getattr(u, 'status', None) is None, users)
    ])

    messages = []
    for user in users:
        path = reverse_lazy(unsubscribe_url, kwargs={'uuid': user.status.uuid})
        context = Context({
            'user': user,
            'unsubscribe_link': request.build_absolute_uri(str(path)),
        })
        message = EmailMultiAlternatives(
            Template(instance.subject).render(context),
            Template(instance.message).render(context),
            from_email,
            [user.email],
        )
        if instance.html_message:
            message.attach_alternative(
                Template(instance.html_message).render(context),
                'text/html',
            )

        messages.append(message)

    with get_connection() as connection:
        try:
            connection.send_messages(messages)
        except Exception as e:
            error_message_template = 'Error while sending notification {}: {}'
            logger.error(error_message_template.format(instance.id, e))
            instance.fail()
        else:
            instance.success()
