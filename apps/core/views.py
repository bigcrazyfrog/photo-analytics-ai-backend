import platform
from collections import namedtuple

import django
from django.conf import settings
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from libs.utils import get_changelog_html, get_latest_version

Changelog = namedtuple("Changelog", ["name", "text", "version", "open_api_ui"])

ARGO_CD_URL_MAPPING = {
    "development": "https://deploy.saritasa.rocks/",
    "prod": "TODO",
}
ARGO_CD_MAPPING = {
    "development": "photo-analytics-backend-dev",
    "prod": "photo-analytics-backend-prod",
}


class AppStatsMixin:
    """Add information about app to context."""

    def get_context_data(self, **kwargs):
        """Load changelog data from files."""
        context = super().get_context_data(**kwargs)
        context.update(
            env=settings.ENVIRONMENT,
            version=get_latest_version("CHANGELOG.md"),
            python_version=platform.python_version(),
            django_version=django.get_version(),
            argo_cd_url=ARGO_CD_URL_MAPPING.get(
                settings.ENVIRONMENT, ARGO_CD_URL_MAPPING["development"],
            ),
            argo_cd_app=ARGO_CD_MAPPING.get(
                settings.ENVIRONMENT, ARGO_CD_MAPPING["development"],
            ),
        )
        return context


class WelcomeView(TemplateView):
    """View for that shows welcome page."""

    template_name = "index.html"


class ChangelogView(AppStatsMixin, TemplateView):
    """Class-based view for that shows version of open_api file on main page.

    Displays the current version of the open_api specification and changelog.

    """

    template_name = "changelog.html"

    def get_context_data(self, **kwargs):
        """Load changelog data from files."""
        context = super().get_context_data(**kwargs)
        context["changelog"] = Changelog(
            name=settings.SPECTACULAR_SETTINGS.get("TITLE"),
            text=get_changelog_html("CHANGELOG.md"),
            version=settings.SPECTACULAR_SETTINGS.get("VERSION"),
            open_api_ui=reverse_lazy("open_api:ui"),
        )
        return context

    def get(self, request, *args, **kwargs):
        if settings.DEBUG or request.user.is_staff:
            return super().get(request, *args, **kwargs)
        return HttpResponseNotFound()
