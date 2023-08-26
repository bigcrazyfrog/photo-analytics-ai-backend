from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from libs.utils import get_latest_version

# https://docs.sentry.io/platforms/python/guides/django/
SENTRY_CONFIG = {
    # Adds django, celery, redis support
    "integrations": (
        DjangoIntegration(),
        CeleryIntegration(),
        RedisIntegration(),
    ),
    "attach_stacktrace": True,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    "send_default_pii": True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    "traces_sample_rate": 1.0,
    # Adds a body of request
    "request_bodies": "always",
    "release": get_latest_version("CHANGELOG.md"),
}
