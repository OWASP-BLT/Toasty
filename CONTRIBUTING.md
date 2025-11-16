# Contributing to Toasty

Thank you for your interest in contributing to Toasty! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project follows the OWASP Code of Conduct. By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, etc.)
- Any relevant logs or error messages

### Suggesting Features

Feature requests are welcome! Please provide:

- A clear and descriptive title
- Detailed description of the proposed feature
- Use cases and benefits
- Any potential drawbacks or considerations

### Pull Requests

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, concise commit messages
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests and linting**
   ```bash
   pytest
   black toasty/
   ruff check toasty/
   mypy toasty/
   ```

4. **Submit your pull request**
   - Provide a clear description of your changes
   - Reference any related issues
   - Ensure CI checks pass

## Development Setup

1. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/Toasty.git
   cd Toasty
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Run tests**
   ```bash
   pytest
   ```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose
- Maximum line length: 120 characters

### Example

```python
def analyze_code(code: str, language: str) -> dict[str, Any]:
    """
    Analyze code for potential issues.

    Args:
        code: Source code to analyze
        language: Programming language of the code

    Returns:
        Dictionary containing analysis results
    """
    # Implementation
    pass
```

## Testing

- Write tests for all new functionality
- Maintain or improve code coverage
- Use descriptive test names
- Mock external API calls

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=toasty --cov-report=html

# Run specific test file
pytest tests/test_webhook.py

# Run specific test
pytest tests/test_webhook.py::test_health_check
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings for all public APIs
- Include examples in documentation
- Keep documentation up-to-date with code changes

## Commit Messages

Follow conventional commit format:

```
type(scope): subject

body

footer
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(handlers): add support for draft PR events

Add handler for draft pull request events to provide
early feedback on work-in-progress changes.

Closes #123
```

## Security

- Never commit secrets or credentials
- Report security vulnerabilities privately
- Follow secure coding practices
- Validate all user inputs

## Questions?

Feel free to open an issue for questions or join our community discussions.

Thank you for contributing to Toasty! 🎉
