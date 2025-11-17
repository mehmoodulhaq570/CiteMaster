# Extractor.py for extracting DOIs from research paper titles using CrossRef API

import requests
import urllib.parse
import csv
from .config import get_config
from .exceptions import (
    DOINotFoundError,
    APIError,
    NetworkError,
    FileFormatError,
    retry_on_failure,
    handle_api_error,
    setup_logging,
)

logger = setup_logging()


@retry_on_failure(
    max_attempts=3,
    delay=1.0,
    exceptions=(requests.RequestException, APIError),
    logger=logger,
)
def get_doi_from_title(title):
    """Fetches the DOI of a research paper using its title via CrossRef API."""
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")

    config = get_config()
    base_url = config.get("crossref_base_url", "https://api.crossref.org/works")
    timeout = config.get("api_timeout", 30)
    mailto = config.get("crossref_mailto", "")

    query = urllib.parse.quote(title)
    search_url = f"{base_url}?query.title={query}&rows=1"

    headers = {}
    if mailto:
        headers["User-Agent"] = f"CiteMaster/0.1.2 (mailto:{mailto})"

    try:
        response = requests.get(search_url, headers=headers, timeout=timeout)
        handle_api_error(response, "CrossRef")

        if response.status_code == 200:
            data = response.json()
            items = data.get("message", {}).get("items", [])
            if items:
                doi = items[0].get("DOI")
                if doi:
                    logger.info(f"DOI found for '{title}': {doi}")
                    return doi

        logger.warning(f"DOI not found for title: '{title}'")
        return "DOI not found"

    except requests.Timeout:
        logger.error(f"Timeout while fetching DOI for: '{title}'")
        raise NetworkError(f"Request timed out after {timeout} seconds")
    except requests.ConnectionError as e:
        logger.error(f"Connection error for title '{title}': {e}")
        raise NetworkError(
            "Could not connect to CrossRef API. Check your internet connection."
        )
    except requests.RequestException as e:
        logger.error(f"Request error for title '{title}': {e}")
        raise NetworkError(f"Network error: {str(e)}")


def process_file(file_path):
    """Reads titles from a TXT or CSV file and extracts their DOIs."""
    import os

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if not (file_path.endswith(".txt") or file_path.endswith(".csv")):
        raise FileFormatError(file_path, "File must be .txt or .csv format")

    dois = {}

    try:
        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                titles = [line.strip() for line in f.readlines() if line.strip()]
        elif file_path.endswith(".csv"):
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                titles = [row[0] for row in reader if row and row[0].strip()]

        logger.info(f"Processing {len(titles)} titles from {file_path}")

        for title in titles:
            try:
                doi = get_doi_from_title(title)
                dois[title] = doi
                print(f"\nTitle: {title}\nDOI: {doi}\n")
            except Exception as e:
                logger.error(f"Error processing title '{title}': {e}")
                dois[title] = "Error: " + str(e)

        return dois

    except UnicodeDecodeError as e:
        logger.error(f"Encoding error reading file {file_path}: {e}")
        raise FileFormatError(
            file_path, "File encoding error. Please ensure the file is UTF-8 encoded."
        )
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        raise


# Example Usage
# title = "Deep Learning for Solar Energy Forecasting: A Review"
# doi = get_doi_from_title(title)
# print("Extracted DOI:", doi)

# Process a file (Uncomment the below line to use with a file)
# process_file("paper_titles.txt")  # For TXT file
# process_file("paper_titles.csv")  # For CSV file
