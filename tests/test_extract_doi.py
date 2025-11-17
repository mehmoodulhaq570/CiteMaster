"""Unit tests for extract_doi module."""

import pytest
from unittest.mock import patch, Mock
from cite_master.extract_doi import get_doi_from_title, process_file


class TestGetDOIFromTitle:
    """Test cases for get_doi_from_title function."""

    @patch("cite_master.extract_doi.requests.get")
    def test_successful_doi_extraction(self, mock_get, mock_crossref_response):
        """Test successful DOI extraction from title."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_crossref_response
        mock_get.return_value = mock_response

        title = "Deep Learning for Solar Energy Forecasting"
        doi = get_doi_from_title(title)

        assert doi == "10.1016/j.renene.2023.001"
        mock_get.assert_called_once()

    @patch("cite_master.extract_doi.requests.get")
    def test_doi_not_found(self, mock_get):
        """Test when DOI is not found."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": {"items": []}}
        mock_get.return_value = mock_response

        title = "Non-existent Paper Title"
        doi = get_doi_from_title(title)

        assert doi == "DOI not found"

    @patch("cite_master.extract_doi.requests.get")
    def test_api_failure(self, mock_get):
        """Test handling of API failure."""
        from cite_master.exceptions import APIError

        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        title = "Test Paper Title"

        # Should raise APIError after retries
        with pytest.raises(APIError):
            doi = get_doi_from_title(title)

    @patch("cite_master.extract_doi.requests.get")
    def test_empty_title(self, mock_get):
        """Test with empty title."""
        title = ""

        # Should raise ValueError for empty title
        with pytest.raises(ValueError, match="Title cannot be empty"):
            doi = get_doi_from_title(title)

    @patch("cite_master.extract_doi.requests.get")
    def test_special_characters_in_title(self, mock_get, mock_crossref_response):
        """Test title with special characters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_crossref_response
        mock_get.return_value = mock_response

        title = "AI & ML: A Review of Deep Learning (2023)"
        doi = get_doi_from_title(title)

        assert doi == "10.1016/j.renene.2023.001"


class TestProcessFile:
    """Test cases for process_file function."""

    @patch("cite_master.extract_doi.get_doi_from_title")
    def test_process_txt_file(self, mock_get_doi, temp_txt_file):
        """Test processing a TXT file."""
        mock_get_doi.return_value = "10.1016/j.test.2023.001"

        dois = process_file(temp_txt_file)

        assert len(dois) == 3
        assert all(doi == "10.1016/j.test.2023.001" for doi in dois.values())
        assert mock_get_doi.call_count == 3

    @patch("cite_master.extract_doi.get_doi_from_title")
    def test_process_csv_file(self, mock_get_doi, temp_csv_file):
        """Test processing a CSV file."""
        mock_get_doi.return_value = "10.1016/j.test.2023.001"

        dois = process_file(temp_csv_file)

        assert len(dois) == 3
        assert mock_get_doi.call_count == 3

    def test_unsupported_file_format(self, tmp_path):
        """Test with unsupported file format."""
        from cite_master.exceptions import FileFormatError

        # Create a PDF file
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_text("dummy content", encoding="utf-8")

        # Should raise FileFormatError
        with pytest.raises(FileFormatError):
            result = process_file(str(pdf_file))

    def test_nonexistent_file(self):
        """Test with non-existent file."""
        with pytest.raises(FileNotFoundError):
            process_file("nonexistent_file.txt")

    @patch("cite_master.extract_doi.get_doi_from_title")
    def test_empty_txt_file(self, mock_get_doi, tmp_path):
        """Test processing an empty TXT file."""
        file_path = tmp_path / "empty.txt"
        file_path.write_text("", encoding="utf-8")

        dois = process_file(str(file_path))

        assert len(dois) == 0
        mock_get_doi.assert_not_called()

    @patch("cite_master.extract_doi.get_doi_from_title")
    def test_txt_file_with_blank_lines(self, mock_get_doi, tmp_path):
        """Test TXT file with blank lines."""
        file_path = tmp_path / "with_blanks.txt"
        content = """Title 1

Title 2


Title 3"""
        file_path.write_text(content, encoding="utf-8")
        mock_get_doi.return_value = "10.1016/j.test.2023.001"

        dois = process_file(str(file_path))

        assert len(dois) == 3
        assert mock_get_doi.call_count == 3
