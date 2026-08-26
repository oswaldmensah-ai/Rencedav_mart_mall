"""
@admin_required — restricts views to users with is_admin=True.
Redirects unauthenticated users to login; 403s non-admin authenticated users.
"""

from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def admin_required(view_func):
    """Decorator: user must be authenticated AND have is_admin=True."""

    @wraps(view_func)
    @login_required(login_url='/accounts/login/')
    def wrapped(request, *args, **kwargs):
        if not request.user.is_admin:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapped
