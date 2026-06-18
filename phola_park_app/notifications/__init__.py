# Compatibility package for notifications — re-export names from flat notification modules

"""phola_park_app.notifications package

Used by code that imports phola_park_app.notifications or specific helpers.
"""

from phola_park_app.notifications import *  # noqa: F401,F403

__all__ = getattr(globals().get("__all__"), "__all__", None) or []
