"""Custom exceptions and error handling for CiteMaster."""

import logging
from typing import Optional, Callable, Any
import time
from functools import wraps


class CiteMasterError(Exception):
    """Base exception for CiteMaster errors."""

    pass


class DOINotFoundError(CiteMasterError):
    """Exception raised when DOI cannot be found for a paper title."""

    def __init__(self, title: str, message: str = None):
        self.title = title
        self.message = message or f"DOI not found for title: '{title}'"
        super().__init__(self.message)


class BibTeXNotFoundError(CiteMasterError):
    """Exception raised when BibTeX cannot be fetched for a DOI."""

    def __init__(self, doi: str, message: str = None):
        self.doi = doi
        self.message = message or f"BibTeX not found for DOI: {doi}"
        super().__init__(self.message)


class APIError(CiteMasterError):
    """Exception raised when API request fails."""

    def __init__(self, api_name: str, status_code: int = None, message: str = None):
        self.api_name = api_name
        self.status_code = status_code
        self.message = message or f"API request to {api_name} failed"
        if status_code:
            self.message += f" (Status code: {status_code})"
        super().__init__(self.message)


class NetworkError(CiteMasterError):
    """Exception raised when network connection fails."""

    def __init__(self, message: str = "Network connection failed"):
        self.message = message
        super().__init__(self.message)


class FileFormatError(CiteMasterError):
    """Exception raised when file format is invalid or unsupported."""

    def __init__(self, file_path: str, message: str = None):
        self.file_path = file_path
        self.message = message or f"Invalid or unsupported file format: {file_path}"
        super().__init__(self.message)


class CitationFormatError(CiteMasterError):
    """Exception raised when citation formatting fails."""

    def __init__(self, format_style: str, message: str = None):
        self.format_style = format_style
        self.message = (
            message
            or f"Invalid citation format: '{format_style}'. Supported formats: APA, MLA, IEEE"
        )
        super().__init__(self.message)


class RateLimitError(CiteMasterError):
    """Exception raised when API rate limit is exceeded."""

    def __init__(self, api_name: str, retry_after: int = None):
        self.api_name = api_name
        self.retry_after = retry_after
        self.message = f"Rate limit exceeded for {api_name}"
        if retry_after:
            self.message += f". Retry after {retry_after} seconds"
        super().__init__(self.message)


def retry_on_failure(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
    logger: Optional[logging.Logger] = None,
) -> Callable:
    """
    Decorator to retry function on failure with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry
        logger: Logger instance for logging retry attempts

    Returns:
        Decorated function with retry logic
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts:
                        if logger:
                            logger.error(
                                f"Function {func.__name__} failed after {max_attempts} attempts: {e}"
                            )
                        raise

                    if logger:
                        logger.warning(
                            f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}. "
                            f"Retrying in {current_delay:.1f}s..."
                        )

                    time.sleep(current_delay)
                    current_delay *= backoff

            # This shouldn't be reached, but just in case
            if last_exception:
                raise last_exception

        return wrapper

    return decorator


def handle_api_error(response, api_name: str = "API") -> None:
    """
    Handle API response errors and raise appropriate exceptions.

    Args:
        response: requests.Response object
        api_name: Name of the API for error messages

    Raises:
        RateLimitError: If rate limit is exceeded (429)
        APIError: For other API errors
    """
    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After")
        retry_after = int(retry_after) if retry_after else None
        raise RateLimitError(api_name, retry_after)
    elif response.status_code >= 400:
        raise APIError(api_name, response.status_code)


def setup_logging(
    log_file: str = "errors.log", level: int = logging.INFO, verbose: bool = False
) -> logging.Logger:
    """
    Setup logging configuration.

    Args:
        log_file: Path to log file
        level: Logging level
        verbose: If True, also log to console

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("cite_master")
    logger.setLevel(level)

    # Remove existing handlers
    logger.handlers = []

    # File handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(level)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler (if verbose)
    if verbose:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger


def get_error_suggestion(error: Exception) -> str:
    """
    Get user-friendly error message and suggestions.

    Args:
        error: Exception instance

    Returns:
        User-friendly error message with suggestions
    """
    if isinstance(error, DOINotFoundError):
        return (
            f"❌ Could not find DOI for: '{error.title}'\n"
            f"   Suggestions:\n"
            f"   • Check if the title is spelled correctly\n"
            f"   • Try simplifying the title (remove subtitles)\n"
            f"   • Verify the paper is published and indexed\n"
        )
    elif isinstance(error, BibTeXNotFoundError):
        return (
            f"❌ Could not fetch BibTeX for DOI: {error.doi}\n"
            f"   Suggestions:\n"
            f"   • Verify the DOI is correct\n"
            f"   • Check if the publisher supports BibTeX export\n"
            f"   • Try again later (temporary API issue)\n"
        )
    elif isinstance(error, NetworkError):
        return (
            f"❌ Network connection failed\n"
            f"   Suggestions:\n"
            f"   • Check your internet connection\n"
            f"   • Verify firewall settings\n"
            f"   • Try again in a few moments\n"
        )
    elif isinstance(error, RateLimitError):
        retry_msg = f" Wait {error.retry_after} seconds." if error.retry_after else ""
        return (
            f"❌ API rate limit exceeded for {error.api_name}\n"
            f"   Suggestion: Slow down your requests.{retry_msg}\n"
        )
    elif isinstance(error, FileFormatError):
        return f"❌ {error.message}\n" f"   Supported formats: .txt, .csv\n"
    elif isinstance(error, CitationFormatError):
        return f"❌ {error.message}\n" f"   Please use: 'apa', 'mla', or 'ieee'\n"
    else:
        return (
            f"❌ An unexpected error occurred: {str(error)}\n"
            f"   Please check errors.log for more details.\n"
        )
