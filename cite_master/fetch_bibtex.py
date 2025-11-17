import requests
from .config import get_config
from .exceptions import (
    BibTeXNotFoundError,
    NetworkError,
    retry_on_failure,
    handle_api_error,
    setup_logging,
)

logger = setup_logging()


@retry_on_failure(
    max_attempts=3, delay=1.0, exceptions=(requests.RequestException,), logger=logger
)
def fetch_bibtex_from_doi(doi):
    """Fetches the BibTeX citation of a research paper using its DOI via CrossRef API."""
    if not doi or doi == "DOI not found":
        logger.warning(f"Cannot fetch BibTeX: Invalid DOI '{doi}'")
        return "BibTeX not found."

    config = get_config()
    timeout = config.get("api_timeout", 30)

    url = f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex"

    try:
        response = requests.get(
            url, headers={"Accept": "application/x-bibtex"}, timeout=timeout
        )

        if response.status_code == 200:
            bibtex = response.text.strip()
            logger.info(f"BibTeX fetched successfully for DOI: {doi}")
            return bibtex
        elif response.status_code == 404:
            logger.warning(f"BibTeX not found for DOI: {doi}")
            return "BibTeX not found."
        else:
            handle_api_error(response, "CrossRef BibTeX")
            return "BibTeX not found."

    except requests.Timeout:
        logger.error(f"Timeout while fetching BibTeX for DOI: {doi}")
        raise NetworkError(f"Request timed out after {timeout} seconds")
    except requests.ConnectionError as e:
        logger.error(f"Connection error for DOI '{doi}': {e}")
        raise NetworkError(
            "Could not connect to CrossRef API. Check your internet connection."
        )
    except requests.RequestException as e:
        logger.error(f"Request error for DOI '{doi}': {e}")
        raise NetworkError(f"Network error: {str(e)}")


# Example Usage
# doi = "10.1111/1758-5899.70003"
# bibtex = fetch_bibtex_from_doi(doi)

# print("BibTeX Citation:")
# print(bibtex)
