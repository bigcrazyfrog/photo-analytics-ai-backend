from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm
from .tasks import send_welcome_message


class SignUpView(CreateView):
    """Register new user view."""

    form_class = RegisterForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("index")

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Redirect user from `sign up` page if he is authorized."""
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: RegisterForm) -> HttpResponse:
        """Authorize user after successful log up."""
        response = super().form_valid(form)
        login(self.request, self.object)

        send_welcome_message(form.data["email"])
        return response
