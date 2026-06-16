import json
from pathlib import Path
import pytest
from src.utils import ensure_dir, load_metadata, save_metadata, setup_logger

def test_setup_logger():
    logger = setup_logger("test_logger")
    assert logger.name == "test_logger"
    assert len(logger.handlers) >= 1

def test_ensure_dir(tmp_path):
    test_dir = tmp_path / "new_dir"
    assert not test_dir.exists()
    returned_dir = ensure_dir(test_dir)
    assert test_dir.exists()
    assert test_dir.is_dir()
    assert returned_dir == test_dir

def test_load_save_metadata(tmp_path):
    meta_file = tmp_path / "metadata.json"
    assert not meta_file.exists()
    
    # Test empty load
    initial_data = load_metadata(meta_file)
    assert initial_data == {"images": []}
    
    # Test saving data
    sample_data = {
        "images": [
            {
                "filename": "img_001.jpg",
                "source": "Unsplash",
                "has_person": True
            }
        ]
    }
    save_metadata(sample_data, meta_file)
    assert meta_file.exists()
    
    # Test loading saved data
    loaded_data = load_metadata(meta_file)
    assert loaded_data == sample_data
