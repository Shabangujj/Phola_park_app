"""Compatibility wrapper — moved to phola_park_app.admin.helpers

Deprecated: use phola_park_app.admin.helpers
"""

import warnings

warnings.warn(
    "phola_park_app.admin_helpers is deprecated; use phola_park_app.admin.helpers",
    DeprecationWarning,
)

from phola_park_app.admin.helpers import *  # noqa: F401,F403
