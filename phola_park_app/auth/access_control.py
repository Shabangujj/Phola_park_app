ROLE_HIERARCHY = {
    "admin": 3,
    "supervisor": 2,
    "user": 1
}

ROLE_PERMISSIONS = {
    "admin": {
        "manage_users",
        "assign_portfolio",
        "view_reports",
        "create_reports",
        "delete_reports",
        "manage_notices"
    },
    "supervisor": {
        "view_reports",
        "create_reports",
        "manage_notices"
    },
    "user": {
        "create_reports"
    }
}
