# Phola Park App (Package README)

This README provides overview documentation specific to the phola_park_app package.

Phola Park is a role-based community management web application built with Flask. The package contains the application factory, models, blueprints, and supporting modules.

## Important paths
- `phola_park_app/__init__.py` — the Flask application factory
- `phola_park_app/model.py` — SQLAlchemy models
- `phola_park_app/extensions.py` — extension instances (db, migrate, login_manager, jwt)
- `phola_park_app/auth` — authentication blueprint and helpers
- `phola_park_app/admin` — admin blueprint and management modules
- `phola_park_app/api` — REST API blueprints

## Local development
Follow the steps in the root README.md to set up a virtual environment, install dependencies, configure environment variables, and run migrations.

## Notes for maintainers
- After migrating flat modules into packages, compatibility wrappers were added to preserve old import paths. These are located at the project root and are deprecated; consider removing them after updating dependent code.
- Ensure `phola_park_app/__init__.py` registers all blueprints from the new package structure.
