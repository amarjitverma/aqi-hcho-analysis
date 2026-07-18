# ============================================================
# Logging Configuration
# ============================================================

"""Logging setup using loguru."""

import sys
import os
from loguru import logger
from datetime import datetime


def setup_logging(log_dir: str = "logs", level: str = "INFO"):
    """
    Setup logging configuration.

    Args:
        log_dir (str): Directory for log files
        level (str): Log level ('DEBUG', 'INFO', 'WARNING', 'ERROR')
    """
    # Create logs directory
    os.makedirs(log_dir, exist_ok=True)

    # Remove default handler
    logger.remove()

    # Add console handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=level,
    )

    # Add file handler
    log_file = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log")
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
    )

    logger.info("Logging configured successfully")
    return logger


# Create default logger instance
logger = setup_logging()


def get_logger():
    """Get the logger instance."""
    return logger


if __name__ == "__main__":
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
