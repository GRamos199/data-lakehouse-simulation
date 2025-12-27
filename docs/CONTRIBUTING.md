# Contributing Guide

Thank you for your interest in contributing to the Data Lakehouse Simulation project! This guide will help you get started.

## 🚀 Getting Started

### 1. Fork & Clone
```bash
git clone https://github.com/yourusername/data-lakehouse-simulation.git
cd data-lakehouse-simulation
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
cp .env.example .env
```

### 3. Install Pre-commit Hooks (Optional but Recommended)
```bash
pip install pre-commit
pre-commit install
```

## 📝 Making Changes

### Before You Start
- Check existing issues and PRs to avoid duplicates
- Create an issue for feature requests before starting work
- Discuss breaking changes in issues first

### Code Style Guidelines

#### Python
- Follow PEP 8 with black formatting (120 char line length)
- Use type hints where possible
- Write docstrings for all public functions/classes

```python
def process_data(input_path: str, output_path: str) -> bool:
    """
    Process raw data and save to output location.
    
    Args:
        input_path: Path to input data file
        output_path: Path to save processed data
        
    Returns:
        True if successful, False otherwise
    """
    pass
```

#### Variable Naming
- Use `snake_case` for variables and functions
- Use `PascalCase` for classes
- Use `UPPER_CASE` for constants

#### Comments
- Write meaningful comments explaining "why", not "what"
- Keep comments up-to-date with code changes

### Running Tests Locally

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_validators.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run security checks
bandit -r src/ scripts/ dags/

# Format code
black src/ scripts/ dags/
isort src/ scripts/ dags/

# Lint code
flake8 src/ scripts/ dags/
```

## 📊 Pull Request Process

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-name
```

### 2. Make Your Changes
- Keep commits focused and atomic
- Write clear commit messages

```
Good:   "Add data validation for weather API responses"
Bad:    "Fixed stuff"

Good:   "Refactor database connection pooling"
Bad:    "Changes"
```

### 3. Ensure Tests Pass
```bash
# Run all checks
pytest tests/ -v
black --check src/
flake8 src/
isort --check-only src/
bandit -r src/
```

### 4. Push and Create PR
```bash
git push origin feature/your-feature-name
```

Then open a PR with:
- Clear title describing the change
- Description of what changed and why
- Link to related issues (e.g., "Closes #123")
- Screenshots for UI changes (if applicable)

### 5. Code Review
- Respond to feedback promptly
- Request re-review after making changes
- Be respectful and constructive

## 🏗️ Project Structure

When adding new features, follow this structure:

```
data-lakehouse-simulation/
├── src/
│   ├── new_module/
│   │   ├── __init__.py
│   │   ├── main_logic.py
│   │   └── utils.py
│   └── __init__.py
├── tests/
│   ├── test_new_module.py
└── README.md (document in main README)
```

## 🔄 Adding New Tests

Tests should be added for:
- New functions and classes
- Bug fixes (write test that fails, then fix)
- Edge cases and error conditions

```python
# Good test structure
def test_valid_input():
    """Test function with valid input."""
    result = process_data("valid.csv")
    assert result is True

def test_invalid_input():
    """Test function with invalid input."""
    result = process_data("invalid.csv")
    assert result is False

def test_missing_file():
    """Test function with missing file."""
    with pytest.raises(FileNotFoundError):
        process_data("nonexistent.csv")
```

## 📚 Documentation

### Update Documentation For:
- New features or API changes
- Configuration options
- Dependencies

### Document in:
- Code docstrings
- README.md (overview)
- IMPROVEMENTS.md (what changed)
- terraform/README.md (infrastructure changes)

## 🐛 Reporting Bugs

Include:
- Python version and OS
- Steps to reproduce
- Expected vs actual behavior
- Relevant logs or error messages
- Screenshots if applicable

Template:
```markdown
## Bug Description
Brief description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python: 3.11
- OS: Linux/macOS/Windows
- Airflow: 2.9.3
```

## ✅ Checklist Before Submitting PR

- [ ] Tests pass locally (`pytest tests/ -v`)
- [ ] Code is formatted (`black src/`)
- [ ] Imports are sorted (`isort src/`)
- [ ] No linting errors (`flake8 src/`)
- [ ] Security checks pass (`bandit -r src/`)
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No breaking changes (or documented if necessary)
- [ ] PR description explains the changes

## 🎯 Types of Contributions

### 🚀 Features
- New functionality or capabilities
- Examples: Add new data source, new transformation

### 🐛 Bug Fixes
- Fixing broken functionality
- Examples: Fix parsing error, handle edge case

### 📚 Documentation
- Improving docs and guides
- Examples: Add usage examples, clarify README

### 🔧 Maintenance
- Code quality improvements
- Examples: Refactor code, update dependencies, add tests

### ⚡ Performance
- Optimizations and efficiency improvements
- Examples: Cache results, parallel processing

## 🚀 Release Process

### Version Numbering (Semantic Versioning)
- **MAJOR**: Breaking changes (1.0.0 → 2.0.0)
- **MINOR**: New features (1.0.0 → 1.1.0)
- **PATCH**: Bug fixes (1.0.0 → 1.0.1)

### Release Steps
1. Update version in `package.json` and code
2. Update CHANGELOG.md
3. Create git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. GitHub Actions automatically builds and releases

## 📞 Getting Help

- **Questions**: Open a Discussion in GitHub
- **Bugs**: Open an Issue with bug template
- **Ideas**: Open an Issue with feature request template
- **Chat**: Check project communication channels

## 💬 Code of Conduct

### Be Respectful
- Treat all community members with respect
- Welcome diverse perspectives and backgrounds
- Critique ideas, not people

### Be Professional
- Use clear and inclusive language
- Provide constructive feedback
- Focus on the issue, not the person

### Be Helpful
- Mentor newcomers
- Answer questions patiently
- Share knowledge generously

## 📖 Additional Resources

- [Python PEP 8 Style Guide](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Semantic Versioning](https://semver.org/)
- [Git Commit Message Best Practices](https://chris.beams.io/posts/git-commit/)

## ⭐ Recognition

Contributors will be recognized in:
- README.md contributors section
- GitHub contributors page
- Release notes for their contributions

## Questions?

Don't hesitate to ask! Open an issue or discussion if you're unsure about anything.

Thank you for contributing! 🙌
