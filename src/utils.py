import json
import logging
import random
import time
from pathlib import Path
from typing import Any, Dict, Optional
import requests

def setup_logger(name: str) -> logging.Logger:
    """Set up a standard logger for the project.

    Args:
        name: Name of the logger.

    Returns:
        logging.Logger: Preconfigured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s]: %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def ensure_dir(path: Path) -> Path:
    """Create directory if it does not exist.

    Args:
        path: Path to the directory.

    Returns:
        Path: The confirmed directory path.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path

def retry_request(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    max_retries: int = 3,
    backoff_factor: float = 2.0,
) -> requests.Response:
    """Perform an HTTP request with exponential backoff retry logic.

    Args:
        url: The request URL.
        headers: Optional request headers.
        params: Optional query parameters.
        max_retries: Maximum number of retries before raising error.
        backoff_factor: Multiplier for exponential backoff delay.

    Returns:
        requests.Response: Successful response object.

    Raises:
        requests.HTTPError: If the request fails after all retries.
    """
    logger = setup_logger("retry_request")
    delay = 1.0
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            response.raise_for_status()
            return response
        except (requests.RequestException, requests.HTTPError) as e:
            if attempt == max_retries - 1:
                raise e
            # Log failure and sleep with jitter
            logger.warning(
                f"Request failed (attempt {attempt + 1}/{max_retries}) for URL: {url}. "
                f"Error: {e}. Retrying in {delay:.1f}s..."
            )
            time.sleep(delay + random.uniform(0.1, 0.5))
            delay *= backoff_factor
    raise requests.RequestException(f"Failed to fetch {url} after {max_retries} attempts.")

def load_metadata(path: Path) -> Dict[str, Any]:
    """Load metadata catalog.

    Args:
        path: Path to the metadata.json file.

    Returns:
        Dict[str, Any]: Parsed metadata dictionary.
    """
    if not path.exists():
        return {"images": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"images": []}

def save_metadata(data: Dict[str, Any], path: Path) -> None:
    """Save metadata catalog atomically.

    Args:
        data: Metadata catalog dictionary.
        path: Target filepath.
    """
    # Use a temporary file to prevent corruption on sudden interruptions
    temp_path = path.with_suffix(".tmp")
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    temp_path.replace(path)
