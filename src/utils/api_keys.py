# ============================================================
# API Key Management
# ============================================================

"""Centralized API key management."""

import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def get_api_key(key_name: str) -> str:
    """
    Get API key from environment.

    Args:
        key_name (str): Name of the API key

    Returns:
        str: API key or None if not found
    """
    api_key = os.getenv(key_name)
    if not api_key:
        logger.warning(f"⚠️ API key '{key_name}' not found in environment")
    return api_key


def get_gee_project() -> str:
    """Get Google Earth Engine project ID."""
    return get_api_key("GEE_PROJECT")


def get_cds_api_key() -> str:
    """Get Copernicus CDS API key."""
    return get_api_key("CDS_API_KEY")


def get_firms_api_key() -> str:
    """Get NASA FIRMS API key."""
    return get_api_key("FIRMS_API_KEY")


def get_openaq_api_key() -> str:
    """Get OpenAQ API key."""
    return get_api_key("OPENAQ_API_KEY")


def check_all_keys() -> bool:
    """Check if all required API keys are set."""
    keys = {
        "GEE_PROJECT": get_gee_project(),
        "CDS_API_KEY": get_cds_api_key(),
        "FIRMS_API_KEY": get_firms_api_key(),
        "OPENAQ_API_KEY": get_openaq_api_key(),
    }

    missing = [k for k, v in keys.items() if not v]
    if missing:
        logger.warning(f"Missing API keys: {', '.join(missing)}")
        return False

    logger.info("✅ All API keys are set")
    return True


if __name__ == "__main__":
    check_all_keys()
