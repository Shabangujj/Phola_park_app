"""Compatibility wrapper — moved to phola_park_app.notifications.helpers

Deprecated: use phola_park_app.notifications.helpers
"""

import warnings

warnings.warn(
    "phola_park_app.notifications is deprecated as a flat module; use phola_park_app.notifications.helpers or routes",
    DeprecationWarning,
)

from phola_park_app.notifications.helpers import *  # noqa: F401,F403
