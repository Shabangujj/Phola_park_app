# Development Setup & Troubleshooting

## Quick Setup

### 1. Clone Repository
```bash
git clone https://github.com/Shabangujj/Phola_park_app.git
cd Phola_park_app
```

### 2. Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your local settings
```

### 5. Database Setup
```bash
flask db upgrade
```

### 6. Run Development Server
```bash
flask run
```

The app will be available at `http://localhost:5000`

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'phola_park_app'`

**Solution:**
```bash
# Make sure you're in the project root directory
pwd  # Should show: .../Phola_park_app

# Reinstall in development mode
pip install -e .
```

### Issue: Database errors / migrations failing

**Solution:**
```bash
# Reset database (development only!)
rm phola_park.db

# Reinitialize
flask db upgrade
```

### Issue: Port 5000 already in use

**Solution:**
```bash
# Use a different port
flask run --port 5001
```

### Issue: Virtual environment not activating

**Solution:**
```bash
# On Windows:
venv\Scripts\activate.bat

# On macOS/Linux:
source venv/bin/activate

# Verify activation (should show (venv) in terminal):
which python  # Should show path with 'venv'
```

### Issue: Import errors in templates

**Solution:**
```bash
# Make sure Flask-SQLAlchemy and other imports are correct
pip list | grep Flask

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Issue: Email configuration not working

**Solution:**
```bash
# Check .env configuration:
# - MAIL_SERVER: smtp.gmail.com
# - MAIL_PORT: 587
# - MAIL_USE_TLS: True
# - Use app-specific password (not regular Gmail password)

# Test email sending in Flask shell:
flask shell
>>> from phola_park_app import create_app
>>> from flask_mail import Message
>>> app = create_app()
>>> with app.app_context():
...     msg = Message('Test', recipients=['test@example.com'])
...     # mail.send(msg)  # Uncomment to test
```

### Issue: Permission denied on uploads folder

**Solution:**
```bash
# Ensure uploads folder exists and has correct permissions
mkdir -p phola_park_app/uploads
chmod 755 phola_park_app/uploads
```

---

## Common Commands

### Database Operations
```bash
# Create new migration after model changes
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Revert last migration
flask db downgrade
```

### Run Tests
```bash
# Install pytest (if not already installed)
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=phola_park_app
```

### Code Quality Checks
```bash
# Linting
flake8 phola_park_app

# Install if needed
pip install flake8
```

### Flask Shell
```bash
# Interactive Python shell with app context
flask shell

# Example:
>>> from phola_park_app.model import User
>>> users = User.query.all()
>>> len(users)
```

---

## Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `FLASK_ENV` | Flask environment | `development` or `production` |
| `SECRET_KEY` | Session encryption | Random 32+ char string |
| `DATABASE_URL` | Database connection | `sqlite:///phola_park.db` |
| `JWT_SECRET_KEY` | JWT token signing | Random string |
| `MAIL_SERVER` | Email server | `smtp.gmail.com` |
| `MAIL_USERNAME` | Email username | `your-email@gmail.com` |
| `MAIL_PASSWORD` | Email password | App-specific password |

---

## Production Deployment

### Before Deploying:
1. Set `FLASK_ENV=production`
2. Generate strong `SECRET_KEY` and `JWT_SECRET_KEY`
3. Use PostgreSQL/MySQL instead of SQLite
4. Enable HTTPS/SSL
5. Set cookie security flags to True
6. Configure proper logging
7. Set up error monitoring (e.g., Sentry)

### Deployment Options:
- **Heroku**: Use Procfile (example provided)
- **AWS/DigitalOcean**: Use Gunicorn with Nginx reverse proxy
- **Docker**: Create Dockerfile for containerization

---

## Getting Help

- **Issues**: Check existing issues or create a new one
- **Documentation**: See README.md and CONTRIBUTING.md
- **Email**: Contact maintainer at shabangujj2014@gmail.com

---

**Happy developing! 🚀**
