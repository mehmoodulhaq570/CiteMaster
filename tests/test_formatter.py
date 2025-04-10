import unittest
from cite_master.formatter import format_citation

class TestCitationFormatter(unittest.TestCase):

    def test_apa_format(self):
        bib_data = {
            "author": "John Doe",
            "title": "Test Paper",
            "year": "2023",
            "journal": "Journal of Testing"
        }
        expected = "Doe, J. (2023). Test Paper. *Journal of Testing*."
        result = format_citation(bib_data, "apa")
        self.assertEqual(result, expected)

    def test_mla_format(self):
        bib_data = {
            "author": "Jane Smith",
            "title": "Another Paper",
            "year": "2022",
            "journal": "MLA Journal"
        }
        expected = "Smith, Jane. \"Another Paper.\" *MLA Journal*, 2022."
        result = format_citation(bib_data, "mla")
        self.assertEqual(result, expected)

    def test_ieee_format(self):
        bib_data = {
            "author": "Alice Johnson",
            "title": "IEEE Paper",
            "year": "2021",
            "journal": "IEEE Transactions"
        }
        expected = "A. Johnson, \"IEEE Paper,\" *IEEE Transactions*, 2021."
        result = format_citation(bib_data, "ieee")
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
