# Compatibility package for auth — re-export helpers defined in auth_helpers.py

"""phola_park_app.auth package

Provides role utilities and any auth-related blueprints in the future.
"""

from phola_park_app.auth_helpers import (
    role_required,
    is_admin,
    is_supervisor,
    is_admin_or_supervisor,
    redirect_by_role,
)

__all__ = [
    "role_required",
    "is_admin",
    "is_supervisor",
    "is_admin_or_supervisor",
    "redirect_by_role",
]
