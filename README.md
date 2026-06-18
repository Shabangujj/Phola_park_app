# Phola Park App

Phola Park is a role-based community management web application built with Flask. It provides residents, supervisors, and administrators with tools to report incidents and service requests, manage portfolios, run surveys, send notifications, and review administrative dashboards and reports.

## Key Features
- User authentication and role-based access (admin, supervisor, resident)
- Incident & service report submission with image uploads
- Admin dashboards for user, report, announcement, and notice management
- Supervisor views filtered by portfolio
- Surveys with response collection and exports
- Notification system (in-app + email helpers)
- REST API (v1) with JWT auth for external integrations
- Services layer and forms for clean separation of concerns

## Tech Stack
- Python, Flask
- Flask-Login, Flask-Migrate, Flask-JWT-Extended
- SQLAlchemy (database models)
- WTForms / Flask-WTF
- SQLite (default dev DB) — replace with Postgres/MySQL in production

## Quick Start (Development)
1. Clone the repo
   ```bash
   git clone https://github.com/Shabangujj/Phola_park_app.git
   cd Phola_park_app
   ```

2. Create and activate a virtualenv
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r phola_park_app/requirements.txt
   ```

4. Copy example env and set secrets
   ```bash
   cp .env.example .env
   # edit .env and set SECRET_KEY, DATABASE_URL, MAIL_* etc.
   ```

5. Initialize database (Flask-Migrate)
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Run the app
   ```bash
   flask run
   ```

## Project Structure (high level)
- phola_park_app/
  - auth/ — authentication blueprints and helpers
  - admin/ — admin blueprints, management, tools and summary
  - notifications/ — notification routes and helpers
  - reports/ — report endpoints and helpers
  - api/ — REST API endpoints
  - services/ — business logic services (BaseService, user/report services)
  - forms/ — WTForms definitions
  - utils/ — helper utilities
  - model.py — SQLAlchemy models
  - extensions.py — Flask extension instances
  - __init__.py — app factory

## Contributing
- Create a branch from main (or the agreed development branch)
- Open a PR with a clear description and tests where appropriate
- Keep changes scoped and add / update migrations if models change

## License
Phola_park_app@jay_and_pro project 

## Contact
Maintainer: Shabangujj — shabangujj2014@gmail.com
