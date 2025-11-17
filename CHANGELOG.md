# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.1.2] - 2025-11-17

### Added

- **Comprehensive test suite** with 39+ unit tests using pytest
- **Configuration management system** with JSON support
  - Configurable API timeouts, retries, and rate limits
  - Customizable output directories and filenames
  - Verbose and quiet modes
- **Advanced error handling** with custom exceptions
  - 7 custom exception types (DOINotFoundError, APIError, NetworkError, etc.)
  - Automatic retry logic with exponential backoff
  - User-friendly error messages with actionable suggestions
- **UI improvements**
  - Color-coded terminal output (success, error, warning, info)
  - Processing statistics (time, speed, success rate)
  - Better progress indicators
  - Enhanced user prompts
- **Comprehensive documentation**
  - CONFIGURATION.md - Configuration guide
  - TESTING.md - Testing guide
  - IMPROVEMENTS.md - Detailed improvements summary
  - QUICKSTART.md - Quick reference guide
  - TEST_REPORT.md - Test results report

### Changed

- **Version management** - Unified version to 0.1.2 across all files
- **Entry points** - Fixed to use correct module path
- **Error handling** - Replaced generic exceptions with specific ones
- **Logging** - Enhanced with structured logging and configurable levels
- **Code organization** - Better module structure and imports

### Fixed

- Version inconsistency between **init**.py and setup files
- Entry point path in setup.py and setup.cfg
- Generic try-except blocks replaced with specific exception handling
- Missing import statements

### Technical Details

- Test coverage: 54% overall (100% on critical modules)
- All 39 unit tests passing
- Integration tests verified
- Ready for production use

---

## [1.1] - 2025-04-10

### Added

- New interactive menu-based UI.
- Support for both single-title and bulk file citation input.
- Export to APA, MLA, and IEEE formats.
- Option to generate and save BibTeX citations.
- CLI-friendly prompts and cleaner output.

### Changed

- Cleaner README format with reduced emoji use.

---

## [1.0] - 2025-04-07

### Added

- Initial implementation for paper citation formatting.
- Supported citation formats: APA, MLA, IEEE.
- Accepts paper title input via prompt.
