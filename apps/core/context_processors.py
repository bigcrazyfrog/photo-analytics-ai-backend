from django.conf import settings


def app_info(request):
    """Prepare general info about app."""
    return {
        "app_url": settings.FRONTEND_URL,
        "app_label": settings.APP_LABEL,
    }
