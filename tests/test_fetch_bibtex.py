"""Unit tests for fetch_bibtex module."""

import pytest
from unittest.mock import patch, Mock
from cite_master.fetch_bibtex import fetch_bibtex_from_doi


class TestFetchBibtexFromDOI:
    """Test cases for fetch_bibtex_from_doi function."""

    @patch("cite_master.fetch_bibtex.requests.get")
    def test_successful_bibtex_fetch(self, mock_get, sample_bibtex):
        """Test successful BibTeX fetching."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = sample_bibtex
        mock_get.return_value = mock_response

        doi = "10.1016/j.renene.2023.001"
        bibtex = fetch_bibtex_from_doi(doi)

        assert "@article{Smith2023" in bibtex
        assert "Deep Learning for Solar Energy Forecasting" in bibtex
        mock_get.assert_called_once()

    @patch("cite_master.fetch_bibtex.requests.get")
    def test_bibtex_not_found(self, mock_get):
        """Test when BibTeX is not found."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        doi = "10.9999/invalid.doi"
        bibtex = fetch_bibtex_from_doi(doi)

        assert bibtex == "BibTeX not found."

    @patch("cite_master.fetch_bibtex.requests.get")
    def test_api_server_error(self, mock_get):
        """Test handling of server error."""
        from cite_master.exceptions import APIError

        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        doi = "10.1016/j.test.2023.001"

        # Should raise APIError after retries
        with pytest.raises(APIError):
            bibtex = fetch_bibtex_from_doi(doi)

    @patch("cite_master.fetch_bibtex.requests.get")
    def test_empty_doi(self, mock_get):
        """Test with empty DOI."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        doi = ""
        bibtex = fetch_bibtex_from_doi(doi)

        assert bibtex == "BibTeX not found."

    @patch("cite_master.fetch_bibtex.requests.get")
    def test_correct_headers_sent(self, mock_get):
        """Test that correct headers are sent in request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "@article{test}"
        mock_get.return_value = mock_response

        doi = "10.1016/j.test.2023.001"
        fetch_bibtex_from_doi(doi)

        args, kwargs = mock_get.call_args
        assert "headers" in kwargs
        assert kwargs["headers"]["Accept"] == "application/x-bibtex"

    @patch("cite_master.fetch_bibtex.requests.get")
    def test_bibtex_with_whitespace(self, mock_get):
        """Test BibTeX with leading/trailing whitespace."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "  \n  @article{test}  \n  "
        mock_get.return_value = mock_response

        doi = "10.1016/j.test.2023.001"
        bibtex = fetch_bibtex_from_doi(doi)

        # Should strip whitespace
        assert bibtex == "@article{test}"

    @patch("cite_master.fetch_bibtex.requests.get")
    def test_network_timeout(self, mock_get):
        """Test handling of network timeout."""
        mock_get.side_effect = Exception("Network timeout")

        doi = "10.1016/j.test.2023.001"

        with pytest.raises(Exception):
            fetch_bibtex_from_doi(doi)
