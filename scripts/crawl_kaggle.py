"""Kaggle fallback dataset download utility for Phase 1.

Downloads and extracts a backup public Kaggle image archive if APIs fail.
"""

import argparse
import os
import shutil
import zipfile
from pathlib import Path
from src.config import DATA_RAW
from src.utils import ensure_dir, load_metadata, save_metadata, setup_logger

logger = setup_logger("crawl_kaggle")

def download_kaggle_dataset(dataset_slug: str, output_dir: Path) -> None:
    """Download and unpack a Kaggle image dataset.

    Args:
        dataset_slug: Kaggle dataset slug (e.g. 'paramaggarwal/fashion-product-images-dataset').
        output_dir: Path to write raw downloads to.
    """
    ensure_dir(output_dir)
    
    # Check for Kaggle CLI installation or configuration
    if not shutil.which("kaggle"):
        logger.error(
            "Kaggle CLI is not installed or not in PATH. "
            "Please run 'pip install kaggle' and set up ~/.kaggle/kaggle.json."
        )
        return

    logger.info(f"Downloading Kaggle dataset: {dataset_slug}...")
    temp_download_dir = output_dir / "kaggle_temp"
    ensure_dir(temp_download_dir)

    try:
        # Run Kaggle command line download
        import subprocess
        cmd = ["kaggle", "datasets", "download", "-d", dataset_slug, "-p", str(temp_download_dir)]
        logger.info(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info(result.stdout)
        
        # Look for the zip file
        zip_files = list(temp_download_dir.glob("*.zip"))
        if not zip_files:
            logger.error("No zip file downloaded from Kaggle.")
            return
            
        zip_filepath = zip_files[0]
        logger.info(f"Extracting {zip_filepath}...")
        with zipfile.ZipFile(zip_filepath, "r") as zip_ref:
            zip_ref.extractall(temp_download_dir)
            
        # Move images over to output_dir and catalog them
        metadata_file = output_dir / "metadata.json"
        metadata = load_metadata(metadata_file)
        
        # Look for images (*.jpg, *.png) recursively in temp extraction
        img_extensions = ["*.jpg", "*.jpeg", "*.png"]
        found_images = []
        for ext in img_extensions:
            found_images.extend(temp_download_dir.rglob(ext))
            
        logger.info(f"Cataloging and moving {len(found_images)} images to {output_dir}...")
        
        count = 0
        for idx, img_path in enumerate(found_images):
            # Form clean name
            new_filename = f"kaggle_{dataset_slug.replace('/', '_')}_{idx:05d}{img_path.suffix.lower()}"
            target_path = output_dir / new_filename
            
            # Copy to raw folder
            shutil.copy2(img_path, target_path)
            
            # Append entry to metadata
            metadata["images"].append({
                "filename": new_filename,
                "source": f"Kaggle: {dataset_slug}",
                "url": f"kaggle://{dataset_slug}/{img_path.name}",
                "resolution": [None, None], # Evaluated at preprocessing or during filtering
                "has_person": None,
                "crawled_at": "manual_download"
            })
            count += 1
            if count % 100 == 0:
                save_metadata(metadata, metadata_file)
                
        save_metadata(metadata, metadata_file)
        logger.info(f"Successfully moved and cataloged {count} images.")
        
    except Exception as e:
        logger.error(f"Error executing Kaggle crawl: {e}")
    finally:
        # Cleanup temporary files
        if temp_download_dir.exists():
            logger.info("Cleaning up Kaggle temporary directories...")
            shutil.rmtree(temp_download_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kaggle fallback dataset crawler")
    parser.add_argument(
        "--dataset", 
        type=str, 
        default="paramaggarwal/fashion-product-images-dataset", 
        help="Kaggle dataset slug"
    )
    parser.add_argument("--output-dir", type=str, default=str(DATA_RAW), help="Output directory")
    args = parser.parse_args()
    
    download_kaggle_dataset(args.dataset, Path(args.output_dir))
