[![Version](https://img.shields.io/badge/version-0.1.2-blue)](https://github.com/mehmoodulhaq570/cite_master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/mehmoodulhaq570/doi_hunter)](https://github.com/mehmoodulhaq570/cite_master/issues)
[![Size](https://img.shields.io/github/repo-size/mehmoodulhaq570/doi_hunter.svg)](https://github.com/mehmooulhaq570/cite_master)
[![Downloads](https://img.shields.io/github/downloads/mehmoodulhaq570/doi_hunter/total.svg)](https://github.com/mehmoodulhaq570/cite_master/releases)

# CiteMaster

**CiteMaster** is a smart Python package that helps you automatically generate formatted citations from research paper titles or files of titles. No more manual DOI searching or formatting—CiteMaster does it all for you!

---

## Features

- Extracts DOI from paper titles using the CrossRef API
- Fetches corresponding BibTeX data
- Formats citations in **APA**, **MLA**, or **IEEE**
- Supports batch citation generation from `.txt` or `.csv` files
- Saves formatted citations and BibTeX entries to text files
- **NEW:** Comprehensive test suite with 39+ unit tests
- **NEW:** Configurable settings via JSON config file
- **NEW:** Advanced error handling with automatic retries
- **NEW:** Custom exceptions with helpful error messages
- **NEW:** Color-coded output and progress statistics
- Progress tracking for batch processing of large lists of papers
- Detailed logging with configurable verbosity

---

## Installation

Clone and install CiteMaster locally:

```bash
git clone https://github.com/mehmoodulhaq570/CiteMaster.git
cd CiteMaster
pip install requirements.txt
```

OR you can use the:

```bash
pip install cite_master
```

> **Note:** Make sure you’re using Python 3.7 or higher.

---

## How to Use

CiteMaster provides an interactive interface.

### Running the Program

```python
from cite_master import main

main()
```

You'll be prompted to input:

- A paper title or a file path (`.txt` or `.csv`)
- A citation format: `apa`, `mla`, or `ieee`
- Whether to include **BibTeX** citations along with formatted ones.
- Whether to save the formatted citations and/or BibTeX entries to output files.

---

### Example 1: Single Paper Title

**Input:**

```
Enter a paper title or provide a file path (txt/csv): Deep Learning for Solar Energy Forecasting: A Review
Enter citation format (apa, mla, ieee): apa
Do you want the BibTeX citation as well? (yes/no): yes
Do you want to save formatted citations to outputs/citations_output.txt? (yes/no): yes
Do you want to save BibTeX entries to outputs/bibtex_output.txt? (yes/no): yes
```

**Output:**

```
DOI: 10.1016/j.rser.2020.109984

BibTeX:
@article{DeepLearning2020,
  title={Deep Learning for Solar Energy Forecasting: A Review},
  author={John Smith and Alice Johnson},
  journal={Renewable and Sustainable Energy Reviews},
  volume={132},
  pages={109984},
  year={2020},
  publisher={Elsevier}
}

Formatted Citation (APA):
Smith, J., & Johnson, A. (2020). Deep Learning for Solar Energy Forecasting: A Review. *Renewable and Sustainable Energy Reviews*, 132, 109984. https://doi.org/10.1016/j.rser.2020.109984
```

The formatted citation and BibTeX entry will be saved to `outputs/citations_output.txt` and `outputs/bibtex_output.txt`.

---

### Example 2: File of Titles

**Input:**

```
Enter a paper title or provide a file path (txt/csv): C:\path\to\your\file\paper_titles.txt
Enter citation format (apa, mla, ieee): mla
Do you want the BibTeX citation as well? (yes/no): no
Do you want to save formatted citations to outputs/citations_output.txt? (yes/no): yes

```

In this case, BibTeX entries will not be fetched, and the formatted citations will be saved to `outputs/citations_output.txt`.

---

## Supported Input Formats

- **.txt file**: One paper title per line
- **.csv file**: First column should contain the titles

**Example `paper_titles.txt`:**

```
Artificial Intelligence for Smart Grids
Machine Learning in Climate Forecasting
Machine Learning in Solar Forecasting
```

---

## Output Files

- **Formatted Citations**: All formatted citations will be saved to `outputs/citations_output.txt`.
- **BibTeX Entries**: BibTeX entries will be saved to `outputs/bibtex_output.txt` if requested.
- **Error Logs**: Any errors during processing will be logged in `errors.log`.

---

## Configuration

CiteMaster now supports custom configuration! Create a `config.json` file:

```bash
python -c "from cite_master.config import Config; Config.create_default_config_file()"
```

Customize settings like:

- API timeouts and retry attempts
- Output directories
- Log file locations
- Color output preferences
- And more!

---

## Testing

CiteMaster includes a comprehensive test suite:

```bash
# Install test dependencies
pip install -r tests/requirements-test.txt

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=cite_master --cov-report=html
```

---

## What's New in v0.1.2

🎉 **Major improvements:**

1. **Comprehensive Testing** - 39+ unit tests with mocking
2. **Configuration System** - Flexible JSON-based configuration
3. **Advanced Error Handling** - Retry logic, custom exceptions, helpful messages
4. **UI Improvements** - Color-coded output, processing statistics
5. **Better Logging** - Structured logging with configurable verbosity

See [CHANGELOG.md](CHANGELOG.md) for complete details.

---

## Uninstalling

```bash
pip uninstall cite-master
```
---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Feel free to open issues or submit pull requests. Suggestions and improvements are welcome!

---

## Acknowledgments

- [CrossRef API](https://www.crossref.org/)
- [BibTeX Format](https://www.bibtex.org/)
- Citation styles follow official formatting guidelines.

---

If you have any suggestion or want to contribute to the project you can reach me out at
<mehmooulhaq1040@gmail.com>

**Made ❤️ by [Mehmood Ul Haq]**




