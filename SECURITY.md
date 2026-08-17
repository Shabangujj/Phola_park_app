# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in Phola Park App, please email **shabangujj2014@gmail.com** with:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

**Please do NOT create public issues for security vulnerabilities.**

We will acknowledge receipt within 48 hours and work on a fix promptly.

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 1.x     | ✅ Yes (Current)   |
| < 1.0   | ❌ No              |

## Security Best Practices

### For Users
- Keep your Flask and dependencies updated
- Use strong passwords for all roles (admin, supervisor, resident)
- Enable 2FA where possible
- Review user access regularly
- Keep `.env` file secure (never commit it)

### For Developers
- Always validate and sanitize user inputs
- Use parameterized queries (SQLAlchemy ORM handles this)
- Keep sensitive data out of logs
- Use HTTPS in production
- Update dependencies regularly: `pip install --upgrade -r requirements.txt`
- Run security checks: `pip install safety` then `safety check`

## Security Headers & Configuration

Ensure production deployment includes:
- HTTPS/TLS encryption
- Secure cookies: `REMEMBER_COOKIE_SECURE=True`
- HTTP-only cookies: `REMEMBER_COOKIE_HTTPONLY=True`
- CSRF protection (Flask-WTF enabled by default)
- CORS restrictions: Set `CORS_ORIGINS` appropriately
- Strong `SECRET_KEY` and `JWT_SECRET_KEY`

## Changelog

All security fixes will be documented in the commit history and releases.

---

**Last Updated:** August 17, 2026
