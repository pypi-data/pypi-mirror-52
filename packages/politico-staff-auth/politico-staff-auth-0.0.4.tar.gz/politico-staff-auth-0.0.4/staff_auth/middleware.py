# Imports from Django.
from django.conf import settings
from django.shortcuts import redirect


# Imports from other dependencies.
from social_django.middleware import SocialAuthExceptionMiddleware
from social_core.exceptions import AuthForbidden


class InvalidWorkspaceErrorMiddleware(SocialAuthExceptionMiddleware):
    """Clear errors when a user logs in via an unsupported workspace.

    Subclass the built-in social auth exception handler to give clearer
    error messaging when someone tries to login using a Slack workspace
    other than the one specified by `SOCIAL_AUTH_SLACK_TEAM`.
    """

    def process_exception(self, request, exception):
        if isinstance(exception, AuthForbidden):
            if hasattr(exception, "backend"):
                request.session["workspaces"] = {
                    "expected": exception.backend.expected_workspace,
                    "observed": exception.backend.observed_workspace,
                }

            return redirect("staff_auth:auth-error")

        return super(InvalidWorkspaceErrorMiddleware, self).get_message(
            request, exception
        )
