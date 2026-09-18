# Changelog

All notable changes to Phola Park App will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Documentation infrastructure (Contributing, Code of Conduct, Security Policy)
- GitHub Actions CI/CD workflow for automated testing
- Issue templates (Bug Report, Feature Request)
- Development setup guide and troubleshooting documentation
- Environment configuration template (.env.example)

### Changed
- Updated .env.example with comprehensive configuration options

### Fixed
- (To be filled as fixes are made)

---

## [1.0.0] - 2025-06-22

### Added
- Initial project setup and structure
- Flask application factory pattern
- Role-based access control (Admin, Supervisor, Resident)
- User authentication with Flask-Login and JWT
- Incident & service report submission with image uploads
- Admin dashboards for user, report, announcement, and notice management
- Supervisor views filtered by portfolio
- Survey system with response collection and exports
- Notification system (in-app + email)
- REST API (v1) with JWT authentication
- Services layer for business logic
- WTForms for form handling
- SQLAlchemy ORM for database models
- Database migrations with Flask-Migrate

### Features
- **User Management**: Create, read, update, delete users with role assignment
- **Reporting System**: Residents can submit incident and service delivery reports
- **Survey Management**: Administrators can create surveys and collect responses
- **Notifications**: System and email notifications for important events
- **Announcements**: Post community announcements and notices
- **Portfolios**: Supervisors manage specific community portfolios
- **Reports Dashboard**: Comprehensive reporting and analytics
- **API Integration**: RESTful API for third-party integrations

---

## Guidelines for Updates

### Version Numbering
- **MAJOR**: Breaking changes to API or core functionality
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes and minor improvements

### When Adding Changes
1. Update this file in the [Unreleased] section
2. Move to appropriate version when releasing
3. Include PR/Issue references when applicable

### Categories
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Features marked for removal
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security patches

### Example Entry
```markdown
### Added
- New user authentication method (#123)
- Email notification templates

### Fixed
- Report submission validation error (#124)
- Database connection timeout issue
```

---

## Release Schedule

Releases are scheduled as needed based on feature completion and bug fixes.

For upcoming features and bug tracking, see [Issues](https://github.com/Shabangujj/Phola_park_app/issues).

---

**Last Updated:** August 17, 2026
