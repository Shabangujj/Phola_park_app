"""Compatibility wrapper — moved to phola_park_app.auth.helpers

Deprecated: use phola_park_app.auth.helpers
"""

import warnings

warnings.warn(
    "phola_park_app.auth_helpers is deprecated; use phola_park_app.auth.helpers",
    DeprecationWarning,
)

from phola_park_app.auth.helpers import *  # noqa: F401,F403
