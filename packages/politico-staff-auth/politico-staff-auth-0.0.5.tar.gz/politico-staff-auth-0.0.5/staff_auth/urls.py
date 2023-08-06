# Imports from Django.  # NOQA
from django.urls import path
from django.views.generic.base import RedirectView


# Imports from staff_auth.
from staff_auth.views import StaffAuthErrorView


app_name = "staff_auth"

urlpatterns = [
    path("error/", StaffAuthErrorView.as_view(), name="auth-error"),
    path(
        "login/",
        RedirectView.as_view(pattern_name="social:begin"),
        dict(backend="slack"),
        name="slack-login",
    ),
]
