# Ponddy Email Notification

Ponddy email notification package.

## Installation

Install with `pip`

```
pip install ponddy-email-notification
```

Add this app to `INSTALLED_APPS` in `settings.py`

```python
INSTALLED_APPS = [
    ...
    'email_notifications',
]
```

## Usage

Migrate database

```
python manage.py migrate
```

Config email in `settings.py` check this at [Django Docs](https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-EMAIL_HOST)


Setup urls in `urls.py`

```python
from django.urls import path

from email_notifications.views import UnsubscribeView, UnsubscribeDoneView


urlpatterns = [
    ...
    path(
        'unsubscribe/<uuid:uuid>/',
        UnsubscribeView.as_view(),
        name='unsubscribe',
    ),
    path(
        'unsubscribe/done/',
        UnsubscribeDoneView.as_view(),
        name='unsubscribe_done',
    ),
]
```

**Now you can send email notification with admin!!!**

Also we support django template, your can get user with `user` and unsubscribe link with `unsubscribe_link`, for example

```
Subject -> 'Hi, {{ user.username }}
Message -> '............ unsubscribe with: {{ unsubscribe_link }}'
HTML message -> '........... <a href="{{ unsubscribe_link }}">Click here to unsubscribe</a>'
```

## Customization

If you want to custom unsubscribe url name (default is `unsubscribe`), add `UNSUBSCRIBE_URL` in `settings.py`

```python
UNSUBSCRIBE_URL='{{ your unsubscribe url name }}'
```

If you want to custom unsubscribe done url name (default is `unsubscribe_done`), config it in `.as_view()` function

```python
UnsubscribeView.as_view(success_url='{{ your unsubscribe done url name }}')
```

If you want to custom templates, config it in `.as_view()` function

```python
UnsubscribeView.as_view(template_name='{{ your template name}}')
UnsubscribeDoneView.as_view(template_name='{{ your template name}}')
```

# Example

If you want to send notification with python script

```python
from django.contrib.auth import get_user_model

from email_notifications.models import Notification
from email_notifications.services import send_notification


User = get_user_model()


notification = Notification.objects.create(
    subject='Hi, {{ user.username }}',
    message='............ unsubscribe with: {{ unsubscribe_link }}',
    html_message='........... <a href="{{ unsubscribe_link }}">Click here to unsubscribe</a>',
)
notification.users.add(User.objects.all())  # We will automatic exclude user, if unsubscribe or no email.
send_notification('http://127.0.0.1:8000', notification)
```

or in view

```python
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from email_notifications.models import Notification
from email_notifications.services import send_notification


User = get_user_model()


def example_view(request):
    notification = Notification.objects.create(
        subject='Hi, {{ user.username }}',
        message='............ unsubscribe with: {{ unsubscribe_link }}',
        html_message='........... <a href="{{ unsubscribe_link }}">Click here to unsubscribe</a>',
    )
    notification.users.add(User.objects.all())  # We will automatic exclude user, if unsubscribe or no email.
    send_notification(request.build_absolute_uri('/'), notification)
    return HttpResponse('ok')
```
