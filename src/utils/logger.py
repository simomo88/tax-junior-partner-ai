"""Logging configuration and setup."""

import logging
import logging.config
from pathlib import Path
from pythonjsonlogger import jsonlogger


def setup_logging(log_path: Path, log_level: str, log_format: str = "json") -> None:
    """Setup logging configuration.
    
    Args:
        log_path: Path for log files
        log_level: Logging level
        log_format: Log format ("json" or "text")
    """
    log_path.mkdir(parents=True, exist_ok=True)

    # Create formatters
    if log_format == "json":
        formatter = jsonlogger.JsonFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # File handler
    file_handler = logging.FileHandler(log_path / "app.log")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Console handler (development)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
