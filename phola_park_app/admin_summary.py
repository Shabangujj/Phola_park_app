"""Compatibility wrapper — moved to phola_park_app.admin.summary

Deprecated: use phola_park_app.admin.summary
"""

import warnings

warnings.warn(
    "phola_park_app.admin_summary is deprecated; use phola_park_app.admin.summary",
    DeprecationWarning,
)

from phola_park_app.admin.summary import *  # noqa: F401,F403
