"""UI utilities for better user experience."""

import time
from typing import Dict, Any
from datetime import datetime
import sys


class Colors:
    """ANSI color codes for terminal output."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    @staticmethod
    def is_supported():
        """Check if terminal supports colors."""
        return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def colorize(text: str, color: str, enabled: bool = True) -> str:
    """
    Colorize text if colors are enabled.

    Args:
        text: Text to colorize
        color: Color code from Colors class
        enabled: Whether colors are enabled

    Returns:
        Colorized text or plain text
    """
    if enabled and Colors.is_supported():
        return f"{color}{text}{Colors.RESET}"
    return text


def print_success(message: str, color_enabled: bool = True) -> None:
    """Print success message in green."""
    print(colorize(f"✅ {message}", Colors.GREEN, color_enabled))


def print_error(message: str, color_enabled: bool = True) -> None:
    """Print error message in red."""
    print(colorize(f"❌ {message}", Colors.RED, color_enabled))


def print_warning(message: str, color_enabled: bool = True) -> None:
    """Print warning message in yellow."""
    print(colorize(f"⚠️  {message}", Colors.YELLOW, color_enabled))


def print_info(message: str, color_enabled: bool = True) -> None:
    """Print info message in blue."""
    print(colorize(f"ℹ️  {message}", Colors.BLUE, color_enabled))


def print_header(message: str, color_enabled: bool = True) -> None:
    """Print header message in bold cyan."""
    if color_enabled and Colors.is_supported():
        print(
            colorize(
                f"\n{Colors.BOLD}{message}{Colors.RESET}", Colors.CYAN, color_enabled
            )
        )
    else:
        print(f"\n{'='*60}\n{message}\n{'='*60}")


class ProcessingStats:
    """Track and display processing statistics."""

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.total_items = 0
        self.successful = 0
        self.failed = 0
        self.errors = []

    def start(self, total_items: int = 0):
        """Start tracking."""
        self.start_time = time.time()
        self.total_items = total_items
        self.successful = 0
        self.failed = 0
        self.errors = []

    def record_success(self):
        """Record a successful item."""
        self.successful += 1

    def record_failure(self, item: str, error: str):
        """Record a failed item."""
        self.failed += 1
        self.errors.append({"item": item, "error": error})

    def end(self):
        """End tracking."""
        self.end_time = time.time()

    def get_elapsed_time(self) -> float:
        """Get elapsed time in seconds."""
        if not self.start_time:
            return 0
        end = self.end_time or time.time()
        return end - self.start_time

    def get_processing_speed(self) -> float:
        """Get processing speed (items per second)."""
        elapsed = self.get_elapsed_time()
        if elapsed == 0:
            return 0
        return (self.successful + self.failed) / elapsed

    def print_summary(self, color_enabled: bool = True):
        """Print processing summary."""
        elapsed = self.get_elapsed_time()
        speed = self.get_processing_speed()

        print_header("📊 Processing Summary", color_enabled)

        print(f"\n⏱️  Total time: {elapsed:.2f} seconds")
        print(f"📈 Processing speed: {speed:.2f} items/second")
        print(f"📝 Total items: {self.total_items}")

        if self.successful > 0:
            print_success(f"Successful: {self.successful}", color_enabled)

        if self.failed > 0:
            print_error(f"Failed: {self.failed}", color_enabled)

            if self.errors and len(self.errors) <= 10:
                print("\nFailed items:")
                for error_info in self.errors:
                    print(f"  • {error_info['item'][:50]}... - {error_info['error']}")
            elif self.errors:
                print(
                    f"\n  {len(self.errors)} items failed. Check errors.log for details."
                )

        success_rate = (
            (self.successful / self.total_items * 100) if self.total_items > 0 else 0
        )
        print(f"\n✓ Success rate: {success_rate:.1f}%")


def format_time_remaining(seconds: float) -> str:
    """
    Format time remaining in human-readable format.

    Args:
        seconds: Seconds remaining

    Returns:
        Formatted time string
    """
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def print_welcome():
    """Print welcome message."""
    print("\n" + "=" * 70)
    print(
        colorize(
            "📚 Welcome to CiteMaster: Automatic Citation Generator!",
            Colors.CYAN + Colors.BOLD,
            True,
        )
    )
    print("=" * 70 + "\n")


def print_goodbye():
    """Print goodbye message."""
    print("\n" + "=" * 70)
    print(colorize("👋 Thank you for using CiteMaster!", Colors.CYAN, True))
    print("=" * 70 + "\n")


def create_progress_bar(current: int, total: int, width: int = 50) -> str:
    """
    Create a text-based progress bar.

    Args:
        current: Current progress
        total: Total items
        width: Width of progress bar

    Returns:
        Progress bar string
    """
    if total == 0:
        return "[" + " " * width + "] 0%"

    percent = current / total
    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percent*100:.1f}%"


def get_file_conflict_name(base_path: str) -> str:
    """
    Get a non-conflicting filename by adding a number suffix.

    Args:
        base_path: Base file path

    Returns:
        Non-conflicting file path
    """
    import os

    if not os.path.exists(base_path):
        return base_path

    base, ext = os.path.splitext(base_path)
    counter = 2

    while os.path.exists(f"{base}_{counter}{ext}"):
        counter += 1

    return f"{base}_{counter}{ext}"


def prompt_yes_no(question: str, default: bool = False) -> bool:
    """
    Prompt user for yes/no response.

    Args:
        question: Question to ask
        default: Default value if user just presses Enter

    Returns:
        True for yes, False for no
    """
    suffix = " [Y/n]: " if default else " [y/N]: "
    while True:
        response = input(question + suffix).strip().lower()

        if not response:
            return default

        if response in ("y", "yes"):
            return True
        elif response in ("n", "no"):
            return False
        else:
            print("Please answer 'yes' or 'no'.")


def prompt_choice(question: str, choices: list, default: str = None) -> str:
    """
    Prompt user to choose from a list of options.

    Args:
        question: Question to ask
        choices: List of valid choices
        default: Default choice if user just presses Enter

    Returns:
        Selected choice
    """
    choices_str = "/".join(choices)
    suffix = f" [{choices_str}]"
    if default:
        suffix += f" (default: {default})"
    suffix += ": "

    while True:
        response = input(question + suffix).strip().lower()

        if not response and default:
            return default

        if response in [c.lower() for c in choices]:
            return response
        else:
            print(f"Please choose from: {', '.join(choices)}")
