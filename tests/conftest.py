"""Pytest configuration and shared fixtures."""

import pytest
import os
import tempfile


@pytest.fixture
def sample_bibtex():
    """Sample BibTeX entry for testing."""
    return """@article{Smith2023,
  author = {Smith, John and Doe, Alice},
  title = {Deep Learning for Solar Energy Forecasting},
  journal = {Renewable Energy},
  volume = {32},
  number = {4},
  pages = {123-130},
  year = {2023},
  doi = {10.1016/j.renene.2023.001}
}"""


@pytest.fixture
def sample_titles():
    """Sample paper titles for testing."""
    return [
        "Deep Learning for Solar Energy Forecasting: A Review",
        "Machine Learning in Climate Change Research",
        "Artificial Intelligence Applications in Renewable Energy",
    ]


@pytest.fixture
def temp_txt_file(tmp_path):
    """Create a temporary text file with paper titles."""
    file_path = tmp_path / "test_papers.txt"
    content = """Deep Learning for Solar Energy Forecasting
Machine Learning in Climate Change Research
Artificial Intelligence Applications in Renewable Energy"""
    file_path.write_text(content, encoding="utf-8")
    return str(file_path)


@pytest.fixture
def temp_csv_file(tmp_path):
    """Create a temporary CSV file with paper titles."""
    file_path = tmp_path / "test_papers.csv"
    content = """Deep Learning for Solar Energy Forecasting
Machine Learning in Climate Change Research
Artificial Intelligence Applications in Renewable Energy"""
    file_path.write_text(content, encoding="utf-8")
    return str(file_path)


@pytest.fixture
def mock_crossref_response():
    """Mock CrossRef API response."""
    return {
        "status": "ok",
        "message-type": "work-list",
        "message": {
            "items": [
                {
                    "DOI": "10.1016/j.renene.2023.001",
                    "title": ["Deep Learning for Solar Energy Forecasting"],
                    "author": [
                        {"given": "John", "family": "Smith"},
                        {"given": "Alice", "family": "Doe"},
                    ],
                    "container-title": ["Renewable Energy"],
                    "volume": "32",
                    "issue": "4",
                    "page": "123-130",
                    "published-print": {"date-parts": [[2023]]},
                }
            ]
        },
    }
