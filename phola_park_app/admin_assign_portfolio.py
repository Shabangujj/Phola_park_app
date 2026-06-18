"""Compatibility wrapper — moved to phola_park_app.admin.manage_portfolios

Deprecated: use phola_park_app.admin.manage_portfolios
"""

import warnings

warnings.warn(
    "phola_park_app.admin_assign_portfolio is deprecated; use phola_park_app.admin.manage_portfolios",
    DeprecationWarning,
)

from phola_park_app.admin.manage_portfolios import *  # noqa: F401,F403
