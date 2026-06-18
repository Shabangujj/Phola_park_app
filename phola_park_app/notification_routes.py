"""Compatibility wrapper — moved to phola_park_app.notifications.routes

Deprecated: use phola_park_app.notifications.routes
"""

import warnings

warnings.warn(
    "phola_park_app.notification_routes is deprecated; use phola_park_app.notifications.routes",
    DeprecationWarning,
)

from phola_park_app.notifications.routes import *  # noqa: F401,F403
