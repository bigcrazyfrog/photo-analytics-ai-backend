from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from imagekit.admin import AdminThumbnail

from apps.core.admin import BaseAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseAdmin, DjangoUserAdmin):
    """UI for User model."""

    ordering = (
        "username",
    )
    avatar_thumbnail = AdminThumbnail(
        image_field="avatar_thumbnail",
    )
    list_display = (
        "avatar_thumbnail",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_superuser",
    )
    list_display_links = (
        "username",
    )
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": (
                    "wide",
                ),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                ),
            },
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "avatar",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
