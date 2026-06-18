# Forms package initializer — export common forms used across the app

"""phola_park_app.forms package

Some code imports `from phola_park_app.forms import CreateUserForm` or other
classes from the flat forms module. Provide a central place which re-exports
known forms from the reorganized location while remaining compatible with
existing imports.
"""

# Preferred locations
try:
    from phola_park_app.forms.auth_forms import (
        RegisterForm,
        LoginForm,
        ReportForm as ReportFormFromAuth,
    )
except Exception:
    # fallback to legacy flat forms.py
    from phola_park_app.forms import (
        RegisterForm,
        LoginForm,
        ReportForm as ReportFormFromLegacy,
    )

# Some modules expect ReportForm to be importable from phola_park_app.forms
try:
    ReportForm = ReportFormFromAuth
except NameError:
    ReportForm = ReportFormFromLegacy  # type: ignore

# CreateUserForm may be defined elsewhere; attempt to import it
try:
    from phola_park_app.forms.user_forms import CreateUserForm
except Exception:
    try:
        from phola_park_app.forms import CreateUserForm  # legacy
    except Exception:
        CreateUserForm = None  # type: ignore

__all__ = [
    "RegisterForm",
    "LoginForm",
    "ReportForm",
    "CreateUserForm",
]
