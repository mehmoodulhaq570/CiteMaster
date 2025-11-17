"""Configuration management for CiteMaster."""

import os
from pathlib import Path
from typing import Dict, Any
import json


class Config:
    """Configuration manager for CiteMaster application."""

    # Default configuration values
    DEFAULTS = {
        # Output settings
        "output_dir": "outputs",
        "citations_filename": "citations_output.txt",
        "bibtex_filename": "bibtex_output.txt",
        "log_filename": "errors.log",
        # API settings
        "api_timeout": 30,  # seconds
        "api_retry_attempts": 3,
        "api_retry_delay": 1,  # seconds
        "api_rate_limit": 50,  # requests per minute
        # Processing settings
        "batch_progress_threshold": 50,  # Show progress bar for files with more than this many titles
        "max_workers": 5,  # For parallel processing
        "cache_enabled": True,
        "cache_expiry_days": 30,
        # CrossRef API settings
        "crossref_base_url": "https://api.crossref.org/works",
        "crossref_mailto": "",  # Optional: Add your email for better API rate limits
        # Output formatting
        "verbose": False,
        "quiet": False,
        "color_output": True,
    }

    def __init__(self, config_path: str = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to configuration file (JSON). If None, uses defaults.
        """
        self._config: Dict[str, Any] = self.DEFAULTS.copy()
        self._config_path = config_path

        if config_path and os.path.exists(config_path):
            self.load_from_file(config_path)

        # Create output directory if it doesn't exist
        self._ensure_output_dir()

    def load_from_file(self, config_path: str) -> None:
        """
        Load configuration from JSON file.

        Args:
            config_path: Path to JSON configuration file
        """
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                self._config.update(user_config)
        except Exception as e:
            print(f"Warning: Could not load config from {config_path}: {e}")
            print("Using default configuration.")

    def save_to_file(self, config_path: str = None) -> None:
        """
        Save current configuration to JSON file.

        Args:
            config_path: Path to save configuration. If None, uses initialized path.
        """
        path = config_path or self._config_path
        if not path:
            raise ValueError("No configuration path specified")

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=4)
        except Exception as e:
            print(f"Error saving configuration: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value

    def update(self, config_dict: Dict[str, Any]) -> None:
        """
        Update multiple configuration values.

        Args:
            config_dict: Dictionary of configuration values to update
        """
        self._config.update(config_dict)

    def _ensure_output_dir(self) -> None:
        """Create output directory if it doesn't exist."""
        output_dir = self.get("output_dir")
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    def get_output_path(self, filename: str) -> str:
        """
        Get full path for output file.

        Args:
            filename: Output filename

        Returns:
            Full path to output file
        """
        return os.path.join(self.get("output_dir"), filename)

    def get_citations_output_path(self) -> str:
        """Get full path for citations output file."""
        return self.get_output_path(self.get("citations_filename"))

    def get_bibtex_output_path(self) -> str:
        """Get full path for BibTeX output file."""
        return self.get_output_path(self.get("bibtex_filename"))

    def get_log_path(self) -> str:
        """Get full path for log file."""
        return self.get("log_filename")

    def to_dict(self) -> Dict[str, Any]:
        """
        Get configuration as dictionary.

        Returns:
            Configuration dictionary
        """
        return self._config.copy()

    @classmethod
    def create_default_config_file(cls, path: str = "config.json") -> None:
        """
        Create a default configuration file.

        Args:
            path: Path to save configuration file
        """
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(cls.DEFAULTS, f, indent=4)
            print(f"Default configuration file created at: {path}")
        except Exception as e:
            print(f"Error creating configuration file: {e}")


# Global configuration instance
_global_config: Config = None


def get_config() -> Config:
    """
    Get global configuration instance.

    Returns:
        Global Config instance
    """
    global _global_config
    if _global_config is None:
        # Try to load from default location
        default_config_path = "config.json"
        if os.path.exists(default_config_path):
            _global_config = Config(default_config_path)
        else:
            _global_config = Config()
    return _global_config


def set_config(config: Config) -> None:
    """
    Set global configuration instance.

    Args:
        config: Config instance to set as global
    """
    global _global_config
    _global_config = config


def reset_config() -> None:
    """Reset global configuration to defaults."""
    global _global_config
    _global_config = None
