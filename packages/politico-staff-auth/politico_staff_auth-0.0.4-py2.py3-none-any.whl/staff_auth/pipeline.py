# Imports from Django.  # NOQA
from django.conf import settings


def promote_staffer_to_staff(backend, user, response, *args, **kwargs):
    """"""
    if backend.name == "slack" and kwargs["is_new"]:
        user.is_staff = True


def promote_manager_to_superuser(backend, user, response, *args, **kwargs):
    """"""
    if not hasattr(settings, "MANAGERS"):
        return

    manager_emails = [mgr_email for mgr_name, mgr_email in settings.MANAGERS]

    if user.email in manager_emails:
        user.is_staff = True
        user.is_superuser = True
