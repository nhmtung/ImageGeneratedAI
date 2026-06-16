# tests/test_crawl_nsfw.py
"""Unit test for NSFW crawling support in crawl_unsplash.py"""
import os
import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Import the function after the module path is ensured
from src.config import DATA_RAW_NSFW
from scripts.crawl_unsplash import crawl_unsplash

@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Path:
    # Create a temporary directory to act as NSFW output dir
    out_dir = tmp_path / "nsfw"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir

def mock_retry_request(url, headers=None, params=None, timeout=15):
    """Mock retry_request to simulate Unsplash API responses and image download."""
    # Determine if this is a search request or an image download based on URL pattern
    if "search/photos" in url:
        # Return a mock response with JSON data
        mock_resp = Mock()
        mock_resp.json.return_value = {
            "results": [
                {
                    "urls": {"regular": "https://example.com/fake_image.jpg"},
                    "width": 1080,
                    "height": 720,
                }
            ]
        }
        return mock_resp
    else:
        # Image download – return content bytes
        mock_resp = Mock()
        mock_resp.content = b"fakeimagedata"
        return mock_resp

def test_crawl_nsfw_creates_file_and_metadata(monkeypatch, temp_output_dir: Path):
    # Ensure environment variable for Unsplash key exists (value not used by mock)
    monkeypatch.setenv("UNSPLASH_KEY", "dummy_key")

    # Patch retry_request used inside crawl_unsplash module via utils
    monkeypatch.setattr("scripts.crawl_unsplash.utils.retry_request", mock_retry_request)
    # Also patch the utility version for completeness
    monkeypatch.setattr("src.utils.retry_request", mock_retry_request)

    # Run crawler with a single keyword and limit 1
    crawl_unsplash(limit=1, output_dir=temp_output_dir, keywords=["test_nsfw"])

    # Verify that an image file was created
    files = list(temp_output_dir.glob("*.jpg"))
    assert len(files) == 1, "NSFW image file should be downloaded"

    # Verify metadata.json exists and contains one entry
    metadata_path = temp_output_dir / "metadata.json"
    assert metadata_path.exists(), "metadata.json should be created"
    metadata = json.loads(metadata_path.read_text())
    assert "images" in metadata and len(metadata["images"]) == 1
    image_entry = metadata["images"][0]
    assert image_entry["filename"] == files[0].name
    assert image_entry["source"] == "Unsplash"
    assert image_entry["url"] == "https://example.com/fake_image.jpg"
