from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.contrib.postgres.fields import CIEmailField
from django.db import models
from django.utils.translation import gettext_lazy as _

from imagekit import models as imagekit_models
from imagekit.processors import ResizeToFill, Transpose

from apps.core.models import BaseModel


class UserManager(DjangoUserManager):
    """Adjusted User manager that works with `username` field."""

    def _create_user(self, username, email, password, **extra_fields):
        """Create and save a user with set username if it is skipped.

        Check the given `USERNAME_FIELD` set. Set `username`
        as `USERNAME_FIELD` if it is skipped. Create user like
        `DjangoUserManager`.

        """
        fields = {
            "username": username,
            "email": email,
            **extra_fields,
        }
        if not fields.get(User.USERNAME_FIELD):
            raise ValueError(f"The given {User.USERNAME_FIELD} must be set")
        fields.update(username=username or fields.get(User.USERNAME_FIELD))
        return super()._create_user(password=password, **fields)

    def create_superuser(
        self,
        username=None,
        email=None,
        password=None,
        **extra_fields,
    ):
        """Create superuser instance (used by `createsuperuser` cmd)."""
        return super().create_superuser(
            username,
            email,
            password,
            **extra_fields,
        )


class User(
    AbstractBaseUser,
    PermissionsMixin,
    BaseModel,
):
    """Custom user model."""

    username = models.CharField(
        verbose_name=_("Username"),
        max_length=30,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name=_("First name"),
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name=_("Last name"),
        max_length=30,
        blank=True,
    )
    email = CIEmailField(
        verbose_name=_("Email address"),
        max_length=254,  # to be compliant with RFCs 3696 and 5321
        unique=True,
    )
    is_staff = models.BooleanField(
        verbose_name=_("Staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site.",
        ),
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active.",
        ),
    )

    avatar = imagekit_models.ProcessedImageField(
        verbose_name=_("Avatar"),
        blank=True,
        null=True,
        upload_to=settings.DEFAULT_MEDIA_PATH,
        max_length=512,
        processors=[Transpose()],
        options={
            "quality": 100,
        },
    )
    avatar_thumbnail = imagekit_models.ImageSpecField(
        source="avatar",
        processors=[
            ResizeToFill(50, 50),
        ],
    )

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        return f"{self.username}"
