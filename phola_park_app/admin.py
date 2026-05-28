"""Compatibility wrapper — moved to phola_park_app.admin.routes

This module is kept for backward compatibility. Import from the new package:
    from phola_park_app.admin.routes import ...

It will be removed in a future release.
"""

import warnings

warnings.warn(
    "phola_park_app.admin is deprecated; use phola_park_app.admin.routes and submodules under phola_park_app.admin",
    DeprecationWarning,
)

# Re-export common names if available
try:
    from phola_park_app.admin.routes import *  # noqa: F401,F403
except Exception:
    # If new module isn't fully populated yet, fail silently to avoid import errors
    pass
