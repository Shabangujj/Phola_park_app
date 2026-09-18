# Phola Park App 🌳

[![Python Tests & Lint](https://github.com/Shabangujj/Phola_park_app/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Shabangujj/Phola_park_app/actions/workflows/python-tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: flake8](https://img.shields.io/badge/Code%20style-flake8-green)](https://flake8.pycqa.org/)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baadc.svg)](CODE_OF_CONDUCT.md)

A community engagement platform for service delivery, reporting, and community management.

**Status**: Active Development | **Version**: 1.0.0

---

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

---

## ✨ Features

### Core Features
- **Role-Based Access Control**: Admin, Supervisor, and Resident roles
- **User Management**: Create, manage, and assign community members
- **Reporting System**: Submit incident and service delivery reports with image uploads
- **Survey Management**: Create surveys, collect responses, and export data
- **Announcements & Notices**: Post community updates and important notices
- **Notification System**: In-app and email notifications
- **Admin Dashboards**: Comprehensive management interfaces
- **REST API**: JSON API with JWT authentication

### Key Capabilities
- Filter reports by portfolio and status
- Track service delivery improvements
- Collect community feedback through surveys
- Maintain communication through announcements
- Role-specific views and permissions

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git
- pip/virtualenv

### Installation

```bash
# 1. Clone repository
git clone https://github.com/Shabangujj/Phola_park_app.git
cd Phola_park_app

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings

# 5. Initialize database
flask db upgrade

# 6. Run development server
flask run
```

Visit `http://localhost:5000` in your browser.

**For detailed setup instructions, see [DEVELOPMENT.md](DEVELOPMENT.md)**

---

## 📁 Project Structure

```
Phola_park_app/
├── phola_park_app/          # Main application package
│   ├── auth/               # Authentication blueprints
│   ├── admin/              # Admin dashboard views
│   ├── reports/            # Report management views
│   ├── surveys/            # Survey functionality
│   ├── notifications/      # Notification system
│   ├── api/                # REST API endpoints
│   ├── services/           # Business logic
│   ├── models/             # Database models
│   ├── forms/              # WTForms definitions
│   ├── utils/              # Helper functions
│   ├── templates/          # Jinja2 templates
│   ├── static/             # CSS, JS, images
│   └── __init__.py         # App factory
├── migrations/             # Database migrations
├── tests/                  # Test suite
├── .github/
│   ├── workflows/          # GitHub Actions CI/CD
│   └── ISSUE_TEMPLATE/     # Issue templates
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
├── CONTRIBUTING.md         # Contribution guidelines
├── DEVELOPMENT.md          # Setup & troubleshooting
├── SECURITY.md            # Security policy
├── CODE_OF_CONDUCT.md     # Community standards
├── CHANGELOG.md           # Version history
└── README.md              # This file
```

---

## 📚 Documentation

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Setup, troubleshooting, and commands
- **[SECURITY.md](SECURITY.md)** - Security policy and best practices
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** - Community standards
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and updates

---

## 🤝 Contributing

We welcome contributions! Please follow our guidelines:

1. Read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
2. Review [CONTRIBUTING.md](CONTRIBUTING.md)
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Make your changes and test them
5. Submit a pull request with a clear description

---

## 🔒 Security

For security concerns:
- **Do NOT** create public issues for security vulnerabilities
- Email: **shabangujj2014@gmail.com** with:
  - Vulnerability description
  - Steps to reproduce
  - Potential impact
  - Suggested fix (if available)

See [SECURITY.md](SECURITY.md) for more details.

---

## 📦 Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-JWT-Extended
- **Database**: SQLite (dev), PostgreSQL/MySQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Forms**: WTForms
- **Email**: Flask-Mail
- **Testing**: pytest, pytest-cov
- **CI/CD**: GitHub Actions
- **Code Quality**: flake8

---

## 📋 Requirements

See `requirements.txt` for complete dependencies. Key packages:

- flask==2.3.0
- flask-sqlalchemy==3.0.0
- flask-login==0.6.0
- flask-jwt-extended==4.4.0
- flask-mail==0.9.1
- flask-migrate==4.0.0
- wtforms==3.0.0
- python-dotenv==1.0.0

---

## 🗺️ Roadmap

### In Progress
- Enhanced analytics dashboard
- Mobile app support
- Advanced filtering and search
- Email templates customization

### Future
- SMS notifications
- Video/media uploads
- Community forums
- Offline mode support

See [Issues](https://github.com/Shabangujj/Phola_park_app/issues) for detailed tracking.

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 👥 Authors & Maintainers

**Lead Developer**: Shabangujj  
📧 Email: shabangujj2014@gmail.com  
🔗 GitHub: [@Shabangujj](https://github.com/Shabangujj)

---

## 🙏 Acknowledgments

- Community feedback and suggestions
- Contributors and testers
- Open-source community

---

## 💬 Get Help

- **Issues**: [GitHub Issues](https://github.com/Shabangujj/Phola_park_app/issues)
- **Email**: shabangujj2014@gmail.com
- **Documentation**: See [DEVELOPMENT.md](DEVELOPMENT.md) for common issues

---

## ⭐ Show Your Support

If you find this project helpful, please consider:
- ⭐ Starring the repository
- 🔀 Sharing with others
- 🤝 Contributing improvements
- 💬 Providing feedback

---

**Last Updated**: August 17, 2026  
**Status**: Active Development 🚀
