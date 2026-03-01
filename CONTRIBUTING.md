# Contributing to Payment Dispute Engine

Thank you for your interest in contributing! This document provides guidelines and instructions.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Getting Started

### Prerequisites
- Python 3.11+
- Git
- Docker (optional, but recommended)

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/payment-dispute-engine.git
   cd payment-dispute-engine
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Making Changes

1. **Write Code**
   - Follow PEP 8 style guidelines
   - Add type hints to functions
   - Write docstrings for complex logic
   - Add comments for why, not what

2. **Add Tests**
   - Write unit tests for new logic
   - Ensure tests pass locally
   - Aim for >80% code coverage
   ```bash
   python backend/tests/test_engine.py
   ```

3. **Update Documentation**
   - Update IMPLEMENTATION.md if architecture changes
   - Update README if user-facing changes
   - Document new API endpoints

4. **Run Quality Checks**
   ```bash
   # Lint (when configured)
   python -m pylint backend/

   # Type checking (when configured)
   python -m mypy backend/
   ```

### Commit Guidelines

**Commit Message Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Build, dependencies, etc.

**Example:**
```
feat: Add evidence validation to disputes

- Validate file types (PDF, PNG, JPG only)
- Check file size limits (< 10MB)
- Extract and store file metadata

Resolves #123
```

**Subject Rules:**
- Use imperative mood ("add" not "adds", "fixed" not "fixes")
- Don't capitalize first letter
- No period at end
- Limit to 50 characters

**Body:**
- Wrap at 72 characters
- Explain what and why, not how
- Reference issues and discussions

## Pull Request Process

1. **Ensure Code Quality**
   - Run tests: `python backend/tests/test_engine.py`
   - All tests pass
   - No linting errors
   - No breaking changes to API

2. **Create Pull Request**
   - Use the PR template (auto-populated)
   - Link related issues
   - Describe changes clearly
   - Include testing details

3. **Code Review**
   - Address reviewer feedback
   - Push additional commits to same branch
   - Request re-review when ready

4. **Merge**
   - Squash commits if requested
   - Ensure all CI checks pass
   - Merge to main

## Testing

### Running Tests
```bash
# All engine tests
python backend/tests/test_engine.py

# Specific test
python -m pytest backend/tests/test_engine.py::test_sla_calculation -v
```

### Writing Tests
```python
def test_your_feature():
    """Describe what you're testing."""
    # Arrange - set up test data
    dispute = create_test_dispute()
    
    # Act - perform the action
    result = process_dispute(dispute)
    
    # Assert - verify the outcome
    assert result.status == "success"
```

**Test Coverage Areas:**
- Happy path (expected behavior)
- Edge cases (boundary conditions)
- Error scenarios (invalid input)
- State transitions (workflow)

## Documentation Standards

### Code Comments
```python
def calculate_sla_deadline(dispute_type, filed_date):
    """Calculate SLA deadline for a dispute.
    
    Args:
        dispute_type: DisputeType enum value
        filed_date: datetime when dispute was filed
        
    Returns:
        datetime: SLA deadline
        
    Raises:
        ValueError: If dispute_type is invalid
    """
```

### Documentation Updates
- Update IMPLEMENTATION.md for architectural changes
- Update README for user-facing changes
- Add docstrings to new functions
- Update API documentation

## Reporting Issues

### Before Creating an Issue
- Search existing issues
- Check documentation
- Run tests to confirm issue

### When Creating an Issue
- Use appropriate issue template
- Be specific and detailed
- Include reproduction steps
- Provide environment info
- Include logs/error messages

## Code Review Checklist

**Reviewers should verify:**
- [ ] Code follows project style
- [ ] Tests are comprehensive
- [ ] No breaking changes
- [ ] Documentation updated
- [ ] Commits are well-organized
- [ ] PR description is clear
- [ ] No security vulnerabilities
- [ ] Performance is acceptable

## Project Structure

```
payment-dispute-engine/
├── backend/
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Business logic
│   │   └── models/      # Data models
│   ├── tests/           # Unit tests
│   └── main.py          # App entry
└── scripts/             # Utility scripts
```

## Areas for Contribution

### Good First Issues
- Documentation improvements
- Test coverage expansion
- Bug fixes with clear reproduction
- Code style improvements

### Advanced Contributions
- Database integration
- Event queue implementation
- Frontend development
- Performance optimization
- Advanced analytics

## Getting Help

- **Questions?** Open an issue with `[QUESTION]` tag
- **Discussion?** Start a discussion in GitHub
- **Bugs?** Use bug report template
- **Ideas?** Use feature request template

## Acknowledgments

Contributors will be recognized in:
- Project README
- Release notes
- GitHub contributors page

## Questions?

If you have questions about contributing, please:
1. Check existing discussions/issues
2. Open a new discussion
3. Ask in issue comments

---

**Thank you for contributing to Payment Dispute Engine!** ❤️
