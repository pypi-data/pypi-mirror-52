# Imports from python.  # NOQA
import warnings


# Imports from Django.
from django.conf import settings


def configure_staff_auth(**kwargs):
    new_globals = {"POLITICO_STAFF_AUTH_ACTIVE": False}

    try:
        new_globals["SOCIAL_AUTH_SLACK_KEY"] = kwargs.get("key")
        new_globals["SOCIAL_AUTH_SLACK_SECRET"] = kwargs.get("secret")
        new_globals["SOCIAL_AUTH_SLACK_TEAM"] = kwargs.get("team")

        new_globals["AUTHENTICATION_BACKENDS"] = (
            "staff_auth.backend.WorkspaceSpecificSlackOAuth2",
            "django.contrib.auth.backends.ModelBackend",
        )

        new_globals["SOCIAL_AUTH_ERROR_LOGIN_URL"] = "staff_auth:auth-error"

        # Allow non-SSL OAuth redirects for local development (where SSL isn't
        # easily available).
        new_globals["SOCIAL_AUTH_REDIRECT_IS_HTTPS"] = not getattr(
            settings, "DEBUG"
        )

        new_globals["SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL"] = True

        new_globals["POLITICO_STAFF_AUTH_ACTIVE"] = True
    except AttributeError:
        warnings.warn(
            "Slack credentials not supplied. Using built-in Django auth instead."
        )

    return new_globals
