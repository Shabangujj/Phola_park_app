"""Compatibility wrapper — moved to phola_park_app.admin.tools

Deprecated: use phola_park_app.admin.tools
"""

import warnings

warnings.warn(
    "phola_park_app.admin_tools is deprecated; use phola_park_app.admin.tools",
    DeprecationWarning,
)

from phola_park_app.admin.tools import *  # noqa: F401,F403
