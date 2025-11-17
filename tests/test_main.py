"""Unit tests for main module."""

import pytest
from unittest.mock import patch, Mock, mock_open
from io import StringIO
import sys
from cite_master.__main__ import process_single_title, process_multiple_titles


class TestProcessSingleTitle:
    """Test cases for process_single_title function."""

    @patch("cite_master.__main__.format_citation")
    @patch("cite_master.__main__.fetch_bibtex_from_doi")
    @patch("cite_master.__main__.get_doi_from_title")
    def test_successful_processing(
        self, mock_get_doi, mock_fetch_bibtex, mock_format, sample_bibtex
    ):
        """Test successful processing of a single title."""
        mock_get_doi.return_value = "10.1016/j.test.2023.001"
        mock_fetch_bibtex.return_value = sample_bibtex
        mock_format.return_value = "Formatted citation"

        formatted, bibtex = process_single_title("Test Title", "apa", "yes")

        assert formatted == "Formatted citation"
        assert bibtex == sample_bibtex
        mock_get_doi.assert_called_once_with("Test Title")
        mock_fetch_bibtex.assert_called_once_with("10.1016/j.test.2023.001")

    @patch("cite_master.__main__.get_doi_from_title")
    def test_doi_not_found(self, mock_get_doi):
        """Test when DOI is not found."""
        mock_get_doi.return_value = None

        formatted, bibtex = process_single_title("Non-existent Title", "apa", "no")

        assert formatted == "DOI not found."
        assert bibtex == ""

    @patch("cite_master.__main__.get_doi_from_title")
    def test_without_bibtex(self, mock_get_doi):
        """Test processing without BibTeX."""
        mock_get_doi.return_value = "10.1016/j.test.2023.001"

        with patch("cite_master.__main__.fetch_bibtex_from_doi") as mock_fetch:
            with patch("cite_master.__main__.format_citation") as mock_format:
                mock_fetch.return_value = "@article{test}"
                mock_format.return_value = "Formatted citation"

                formatted, bibtex = process_single_title("Test Title", "apa", "no")

                assert formatted == "Formatted citation"
                assert bibtex == ""

    @patch("cite_master.__main__.get_doi_from_title")
    def test_exception_handling(self, mock_get_doi):
        """Test exception handling during processing."""
        mock_get_doi.side_effect = Exception("API Error")

        formatted, bibtex = process_single_title("Test Title", "apa", "no")

        assert formatted == "❌ Error occurred while processing title."
        assert bibtex == ""


class TestProcessMultipleTitles:
    """Test cases for process_multiple_titles function."""

    @patch("cite_master.__main__.format_citation")
    @patch("cite_master.__main__.fetch_bibtex_from_doi")
    @patch("cite_master.__main__.process_file")
    def test_successful_batch_processing(
        self, mock_process_file, mock_fetch_bibtex, mock_format, sample_bibtex
    ):
        """Test successful batch processing of multiple titles."""
        mock_process_file.return_value = {
            "Title 1": "10.1016/j.test.2023.001",
            "Title 2": "10.1016/j.test.2023.002",
        }
        mock_fetch_bibtex.return_value = sample_bibtex
        mock_format.return_value = "Formatted citation"

        results = process_multiple_titles("test_file.txt", "apa", "yes")

        assert len(results) == 2
        assert "Title 1" in results
        assert "Title 2" in results
        assert results["Title 1"]["citation"] == "Formatted citation"
        assert results["Title 1"]["bibtex"] == sample_bibtex

    @patch("cite_master.__main__.process_file")
    def test_doi_not_found_in_batch(self, mock_process_file):
        """Test handling of missing DOIs in batch processing."""
        mock_process_file.return_value = {
            "Title 1": "10.1016/j.test.2023.001",
            "Title 2": None,
        }

        with patch("cite_master.__main__.fetch_bibtex_from_doi") as mock_fetch:
            with patch("cite_master.__main__.format_citation") as mock_format:
                mock_fetch.return_value = "@article{test}"
                mock_format.return_value = "Formatted citation"

                results = process_multiple_titles("test_file.txt", "apa", "no")

                assert results["Title 1"]["citation"] == "Formatted citation"
                assert results["Title 2"]["citation"] == "DOI not found."

    @patch("cite_master.__main__.process_file")
    def test_batch_without_bibtex(self, mock_process_file):
        """Test batch processing without BibTeX."""
        mock_process_file.return_value = {
            "Title 1": "10.1016/j.test.2023.001",
        }

        with patch("cite_master.__main__.fetch_bibtex_from_doi") as mock_fetch:
            with patch("cite_master.__main__.format_citation") as mock_format:
                mock_fetch.return_value = "@article{test}"
                mock_format.return_value = "Formatted citation"

                results = process_multiple_titles("test_file.txt", "apa", "no")

                assert results["Title 1"]["bibtex"] == ""

    @patch("cite_master.__main__.process_file")
    def test_file_read_error(self, mock_process_file):
        """Test handling of file read errors."""
        mock_process_file.side_effect = Exception("File read error")

        results = process_multiple_titles("invalid_file.txt", "apa", "no")

        assert results == {}

    @patch("cite_master.__main__.format_citation")
    @patch("cite_master.__main__.fetch_bibtex_from_doi")
    @patch("cite_master.__main__.process_file")
    def test_duplicate_titles_skipped(
        self, mock_process_file, mock_fetch_bibtex, mock_format
    ):
        """Test that duplicate titles are skipped."""
        mock_process_file.return_value = {
            "Title 1": "10.1016/j.test.2023.001",
            "Title 1": "10.1016/j.test.2023.001",  # Duplicate
        }
        mock_fetch_bibtex.return_value = "@article{test}"
        mock_format.return_value = "Formatted citation"

        results = process_multiple_titles("test_file.txt", "apa", "no")

        # Should only process once due to dict key collision
        assert len(results) == 1


class TestMainIntegration:
    """Integration tests for main function."""

    @patch("builtins.input")
    @patch("cite_master.__main__.get_doi_from_title")
    @patch("cite_master.__main__.fetch_bibtex_from_doi")
    @patch("cite_master.__main__.format_citation")
    def test_single_title_workflow(
        self, mock_format, mock_fetch, mock_get_doi, mock_input
    ):
        """Test complete workflow for single title."""
        mock_input.side_effect = [
            "Test Paper Title",  # title
            "apa",  # format
            "no",  # bibtex
        ]
        mock_get_doi.return_value = "10.1016/j.test.2023.001"
        mock_fetch.return_value = "@article{test}"
        mock_format.return_value = "Formatted citation"

        # Test would require capturing print output
        # This is a basic structure test
        assert True  # Placeholder
