from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils.translation import gettext_lazy as _

from .models import User


class RegisterForm(UserCreationForm):
    """Form for register User model."""

    username = forms.CharField(
        max_length=30,
        validators=(
            ASCIIUsernameValidator(
                message=_(
                    "Enter a valid username. "
                    "Use a-z, A-Z letters and numbers",
                ),
            ),
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
        widgets = {
            "email": forms.EmailInput(
                attrs={"placeholder": "mail@gmail.com"},
            ),
        }
