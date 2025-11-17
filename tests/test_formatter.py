"""Unit tests for formatter module."""

import pytest
from cite_master.formatter import format_citation


class TestFormatCitation:
    """Test cases for format_citation function."""

    def test_apa_format(self, sample_bibtex):
        """Test APA citation formatting."""
        citation = format_citation(sample_bibtex, "apa")

        assert "Smith, John & Doe, Alice" in citation
        assert "(2023)" in citation
        assert "Deep Learning for Solar Energy Forecasting" in citation
        assert "*Renewable Energy*" in citation
        assert "*32*(4)" in citation
        assert "123-130" in citation
        assert "https://doi.org/10.1016/j.renene.2023.001" in citation

    def test_mla_format(self, sample_bibtex):
        """Test MLA citation formatting."""
        citation = format_citation(sample_bibtex, "mla")

        assert "Smith, John, Doe, Alice" in citation
        assert '"Deep Learning for Solar Energy Forecasting."' in citation
        assert "*Renewable Energy*" in citation
        assert "vol. 32" in citation
        assert "no. 4" in citation
        assert "2023" in citation
        assert "pp. 123-130" in citation
        assert "https://doi.org/10.1016/j.renene.2023.001" in citation

    def test_ieee_format(self, sample_bibtex):
        """Test IEEE citation formatting."""
        citation = format_citation(sample_bibtex, "ieee")

        # Check for authors in IEEE format (should be comma-separated)
        assert "Smith" in citation and "Doe" in citation
        assert '"Deep Learning for Solar Energy Forecasting,"' in citation
        assert "*Renewable Energy*" in citation
        assert "vol. 32" in citation
        assert "no. 4" in citation
        assert "2023" in citation
        assert "doi: 10.1016/j.renene.2023.001" in citation

    def test_invalid_style(self, sample_bibtex):
        """Test with invalid citation style."""
        from cite_master.exceptions import CitationFormatError

        # Should raise CitationFormatError
        with pytest.raises(CitationFormatError):
            citation = format_citation(sample_bibtex, "invalid_style")

    def test_case_insensitive_style(self, sample_bibtex):
        """Test that style parameter is case insensitive."""
        citation_upper = format_citation(sample_bibtex, "APA")
        citation_lower = format_citation(sample_bibtex, "apa")
        citation_mixed = format_citation(sample_bibtex, "ApA")

        assert citation_upper == citation_lower == citation_mixed

    def test_missing_optional_fields(self):
        """Test with BibTeX missing optional fields."""
        minimal_bibtex = """@article{Test2023,
  author = {Test Author},
  title = {Test Title},
  journal = {Test Journal},
  year = {2023}
}"""
        citation = format_citation(minimal_bibtex, "apa")

        assert "Test Author" in citation
        assert "Test Title" in citation
        assert "Test Journal" in citation
        assert "2023" in citation

    def test_single_page_number(self):
        """Test with single page number."""
        single_page_bibtex = """@article{Test2023,
  author = {Test Author},
  title = {Test Title},
  journal = {Test Journal},
  volume = {10},
  number = {1},
  pages = {42},
  year = {2023},
  doi = {10.1000/test}
}"""
        citation = format_citation(single_page_bibtex, "ieee")

        # Should use "p." for single page
        assert "p. 42" in citation

    def test_page_range(self):
        """Test with page range."""
        page_range_bibtex = """@article{Test2023,
  author = {Test Author},
  title = {Test Title},
  journal = {Test Journal},
  volume = {10},
  number = {1},
  pages = {42-50},
  year = {2023},
  doi = {10.1000/test}
}"""
        citation = format_citation(page_range_bibtex, "ieee")

        # Should use "pp." for page range
        assert "pp. 42-50" in citation

    def test_multiple_authors_ieee(self):
        """Test IEEE format with multiple authors."""
        multi_author_bibtex = """@article{Test2023,
  author = {John Smith and Alice Doe and Bob Jones},
  title = {Test Title},
  journal = {Test Journal},
  volume = {10},
  number = {1},
  pages = {42-50},
  year = {2023},
  doi = {10.1000/test}
}"""
        citation = format_citation(multi_author_bibtex, "ieee")

        # Should have "and" before last author
        assert "and" in citation

    def test_unknown_author(self):
        """Test with missing author field."""
        no_author_bibtex = """@article{Test2023,
  title = {Test Title},
  journal = {Test Journal},
  year = {2023}
}"""
        citation = format_citation(no_author_bibtex, "apa")

        assert "Unknown Author" in citation

    def test_special_characters_in_title(self):
        """Test with special characters in title."""
        special_char_bibtex = """@article{Test2023,
  author = {Test Author},
  title = {AI & ML: A Review of Deep Learning (2023)},
  journal = {Test Journal},
  year = {2023}
}"""
        citation = format_citation(special_char_bibtex, "apa")

        assert "AI & ML: A Review of Deep Learning (2023)" in citation
