from .extract_doi import get_doi_from_title, process_file
from .fetch_bibtex import fetch_bibtex_from_doi
from .formatter import format_citation
from .config import Config, get_config, set_config
from .exceptions import (
    CiteMasterError,
    DOINotFoundError,
    BibTeXNotFoundError,
    APIError,
    NetworkError,
    FileFormatError,
    CitationFormatError,
    RateLimitError,
)

__all__ = [
    "get_doi_from_title",
    "process_file",
    "fetch_bibtex_from_doi",
    "format_citation",
    "Config",
    "get_config",
    "set_config",
    "CiteMasterError",
    "DOINotFoundError",
    "BibTeXNotFoundError",
    "APIError",
    "NetworkError",
    "FileFormatError",
    "CitationFormatError",
    "RateLimitError",
]

__version__ = "0.1.2"
