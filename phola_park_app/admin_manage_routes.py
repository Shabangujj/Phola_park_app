"""Compatibility wrapper — moved to phola_park_app.admin.manage_routes

Deprecated: use phola_park_app.admin.manage_routes
"""

import warnings

warnings.warn(
    "phola_park_app.admin_manage_routes is deprecated; use phola_park_app.admin.manage_routes",
    DeprecationWarning,
)

from phola_park_app.admin.manage_routes import *  # noqa: F401,F403
