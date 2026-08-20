"""Compatibility wrapper — moved to phola_park_app.admin.manage_users

Deprecated: use phola_park_app.admin.manage_users
"""

import warnings

warnings.warn(
    "phola_park_app.admin_user_management is deprecated; use phola_park_app.admin.manage_users",
    DeprecationWarning,
)

from phola_park_app.admin.manage_users import *  # noqa: F401,F403
