from django.contrib import admin
from django.urls import include, path

from apps.core import views
from libs.health_checks import liveness_check

from .api_versions import urlpatterns as api_urlpatterns
from .debug import urlpatterns as debug_urlpatterns

urlpatterns = [
    path("", views.WelcomeView.as_view(), name="index"),
    path(
        "accounts/",
        include("django.contrib.auth.urls"),
        name="accounts",
    ),
    path("accounts/", include("apps.users.urls"), name="accounts"),
    path("changelog/", views.ChangelogView.as_view(), name="changelog"),
    path("mission-control-center/", admin.site.urls),
    # Django Health Check url
    # See more details: https://pypi.org/project/django-health-check/
    # Custom checks at lib/health_checks
    path("health/", include("health_check.urls")),
    path("liveness/", liveness_check.liveness_check, name="liveness"),
]

urlpatterns += api_urlpatterns
urlpatterns += debug_urlpatterns
