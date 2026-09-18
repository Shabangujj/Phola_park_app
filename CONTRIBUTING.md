# Contributing to Phola Park App

Thank you for your interest in contributing to Phola Park App! This document provides guidelines and instructions for contributing.

## Code of Conduct
Be respectful, inclusive, and professional in all interactions.

## Getting Started

### Prerequisites
- Python 3.8+
- Git
- Virtual environment tool (venv or virtualenv)

### Setup Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/Phola_park_app.git
   cd Phola_park_app
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your local configuration
   ```

5. **Initialize Database**
   ```bash
   flask db upgrade
   ```

6. **Run Development Server**
   ```bash
   flask run
   ```

## Workflow

### Creating a Branch
- Create a feature branch from `main`:
  ```bash
  git checkout -b feature/your-feature-name
  ```
- Use descriptive branch names: `feature/add-user-notifications`, `bugfix/fix-report-filtering`, etc.

### Making Changes
- Keep commits focused and atomic
- Write clear, descriptive commit messages
- Follow the existing code style and conventions
- Add or update migrations if you modify database models:
  ```bash
  flask db migrate -m "Your migration message"
  flask db upgrade
  ```

### Testing
- Test your changes locally before pushing
- Verify the app runs without errors:
  ```bash
  flask run
  ```

### Opening a Pull Request
1. Push your branch to your fork
2. Open a PR against `main` with a clear title and description
3. Reference related issues: `Closes #123`
4. Include screenshots if UI changes are involved
5. Ensure your PR passes all checks

## PR Guidelines

### Title Format
- `[FEATURE] Add user notification system`
- `[BUGFIX] Fix report submission validation`
- `[DOCS] Update README setup instructions`

### Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #(issue number)

## Changes
- Change 1
- Change 2

## Testing
Describe how you tested these changes

## Screenshots (if applicable)
Add screenshots for UI changes
```

## Code Style

### Python
- Follow PEP 8 conventions
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and modular

### Database Models
- Use descriptive model and field names
- Include timestamps (created_at, updated_at)
- Add relationships clearly
- Use appropriate validators

### Flask Routes
- Keep routes in appropriate blueprints
- Use clear function names
- Add route docstrings
- Validate inputs before processing

## Reporting Issues

### Before Creating an Issue
- Check if the issue already exists
- Verify it's not a question better suited for discussions

### Creating a Bug Report
- Use the Bug Report template
- Provide clear steps to reproduce
- Include environment details
- Add screenshots if applicable

### Creating a Feature Request
- Use the Feature Request template
- Clearly describe the problem and solution
- Consider the user impact
- Add user story when applicable

## Project Structure

When adding new features, follow the existing structure:
- **auth/** - Authentication and login logic
- **admin/** - Admin dashboard and management
- **reports/** - Report submission and viewing
- **notifications/** - Notification system
- **api/** - REST API endpoints
- **services/** - Business logic
- **forms/** - WTForms definitions
- **utils/** - Helper functions

## Questions?

- Open an issue with your question
- Contact the maintainer: shabangujj2014@gmail.com

## Recognition

Contributors will be recognized in the project documentation for significant contributions.

---

Happy contributing! 🎉
