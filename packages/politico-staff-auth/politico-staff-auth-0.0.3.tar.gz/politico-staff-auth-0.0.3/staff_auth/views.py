# Imports from Django.  # NOQA
from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import TemplateView


class StaffAuthErrorView(View):
    def get(self, request, *args, **kwargs):
        workspaces = request.session.pop(
            "workspaces",
            {
                "observed": "",
                "expected": getattr(settings, "SOCIAL_AUTH_SLACK_TEAM", ""),
            },
        )
        context = {"workspaces": workspaces}

        return render(request, "staff_auth/auth-error.html", context=context)
