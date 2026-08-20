# Compatibility package for admin — re-export names from flat admin.py

"""phola_park_app.admin package

This package provides a compatibility layer for code that imports
from phola_park_app.admin.* while keeping the existing flat files working.
"""

from phola_park_app.admin import (
    admin_bp,
    get_all_user,
    get_user,
    create_user,
    update_user,
    delete_user,
    get_all_reports,
    get_reports_by_portfolio,
)

__all__ = [
    "admin_bp",
    "get_all_user",
    "get_user",
    "create_user",
    "update_user",
    "delete_user",
    "get_all_reports",
    "get_reports_by_portfolio",
]
