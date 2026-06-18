"""Compatibility wrapper — moved to phola_park_app.forms.base_forms

Deprecated: use phola_park_app.forms.base_forms
"""

import warnings

warnings.warn(
    "phola_park_app.forms is deprecated as a flat module; use phola_park_app.forms.base_forms",
    DeprecationWarning,
)

from phola_park_app.forms.base_forms import *  # noqa: F401,F403
