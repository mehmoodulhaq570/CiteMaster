# Running Tests for CiteMaster

This guide explains how to run the test suite for CiteMaster.

## Installation

First, install the test dependencies:

```bash
pip install -r tests/requirements-test.txt
```

Or install the development version with test dependencies:

```bash
pip install -e ".[dev]"
```

## Running Tests

### Run all tests

```bash
pytest tests/
```

### Run with verbose output

```bash
pytest tests/ -v
```

### Run with coverage report

```bash
pytest tests/ --cov=cite_master --cov-report=html
```

This will generate an HTML coverage report in `htmlcov/index.html`.

### Run specific test file

```bash
pytest tests/test_extract_doi.py
```

### Run specific test

```bash
pytest tests/test_extract_doi.py::TestGetDOIFromTitle::test_successful_doi_extraction
```

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Shared fixtures and configuration
├── test_extract_doi.py      # Tests for DOI extraction
├── test_fetch_bibtex.py     # Tests for BibTeX fetching
├── test_formatter.py        # Tests for citation formatting
├── test_main.py             # Tests for main application logic
└── requirements-test.txt    # Test dependencies
```

## Writing Tests

When adding new features, please add corresponding tests. Tests should:

1. Use descriptive names that explain what they test
2. Include docstrings explaining the test purpose
3. Use appropriate fixtures from `conftest.py`
4. Mock external API calls
5. Test both success and failure cases

Example:

```python
def test_my_feature(mock_api):
    """Test that my feature works correctly."""
    # Arrange
    input_data = "test"

    # Act
    result = my_function(input_data)

    # Assert
    assert result == "expected"
```

## Continuous Integration

Tests are automatically run on every push via GitHub Actions (if configured).

## Troubleshooting

### Import Errors

If you encounter import errors, make sure you've installed the package:

```bash
pip install -e .
```

### Mock Issues

If API mocks aren't working, check that you're patching the correct module path:

```python
@patch('cite_master.extract_doi.requests.get')  # Correct
# Not: @patch('requests.get')  # Incorrect
```

### Coverage Not Working

Ensure pytest-cov is installed:

```bash
pip install pytest-cov
```
