"""YOLOv8 person filtering utility for Phase 1 raw datasets.

Identifies if an image contains a person with high confidence (>=0.7).
Rejected images are shifted to data/_rejected/.
"""

import argparse
from pathlib import Path
from PIL import Image
from ultralytics import YOLO
from src.config import DATA_RAW, DATA_REJECTED, PERSON_CONFIDENCE_THRESHOLD
from src.utils import ensure_dir, load_metadata, save_metadata, setup_logger

logger = setup_logger("filter_person")

def filter_images(raw_dir: Path, rejected_dir: Path) -> None:
    """Filter downloaded images for human presence using YOLOv8n on CPU.

    Args:
        raw_dir: Path containing raw images and metadata.json.
        rejected_dir: Path to move images without humans to.
    """
    metadata_file = raw_dir / "metadata.json"
    if not metadata_file.exists():
        logger.error(f"metadata.json does not exist at {raw_dir}. Please run crawl scripts first.")
        return

    ensure_dir(raw_dir)
    ensure_dir(rejected_dir)
    
    metadata = load_metadata(metadata_file)
    images = metadata.get("images", [])
    if not images:
        logger.info("No images found in metadata catalog.")
        return

    logger.info("Initializing YOLOv8n model on CPU...")
    # Load model (auto-downloads lightweight yolov8n.pt if not present)
    model = YOLO("yolov8n.pt")
    
    updated_images = []
    rejected_count = 0
    approved_count = 0

    for idx, item in enumerate(images):
        filename = item.get("filename")
        filepath = raw_dir / filename
        
        # Handle cases where image is already checked or missing
        if not filepath.exists():
            # If it's already in rejected folder, keep metadata status
            rejected_filepath = rejected_dir / filename
            if rejected_filepath.exists():
                item["has_person"] = False
                updated_images.append(item)
            continue
            
        # If has_person was already evaluated to True, keep it to allow resuming
        if item.get("has_person") is True:
            updated_images.append(item)
            approved_count += 1
            continue

        try:
            # Load resolution if it was missing from metadata API details
            with Image.open(filepath) as img:
                width, height = img.size
                item["resolution"] = [width, height]

            # Run inference strictly on CPU
            results = model.predict(source=filepath, device="cpu", verbose=False)
            
            has_person = False
            best_conf = 0.0
            person_count = 0
            
            # Analyze detected bounding boxes
            if len(results) > 0:
                boxes = results[0].boxes
                for box in boxes:
                    class_id = int(box.cls[0].item())
                    conf = float(box.conf[0].item())
                    # YOLO class '0' stands for 'person'
                    if class_id == 0:
                        person_count += 1
                        if conf > best_conf:
                            best_conf = conf
                        if conf >= PERSON_CONFIDENCE_THRESHOLD:
                            has_person = True

            item["has_person"] = has_person
            
            if has_person:
                logger.info(f"[{idx+1}/{len(images)}] APPROVED: {filename} (Conf: {best_conf:.2f}, Count: {person_count})")
                approved_count += 1
                updated_images.append(item)
            else:
                logger.info(f"[{idx+1}/{len(images)}] REJECTED: {filename} (No human with high confidence)")
                # Move physical file to rejected folder
                target_path = rejected_dir / filename
                filepath.replace(target_path)
                rejected_count += 1
                updated_images.append(item)

        except Exception as e:
            logger.error(f"Failed to process image {filename}: {e}")
            # Keep in raw list to prevent loss, but set has_person as False
            item["has_person"] = False
            updated_images.append(item)

        # Periodically save progress to avoid loss
        if (idx + 1) % 20 == 0:
            metadata["images"] = updated_images
            save_metadata(metadata, metadata_file)

    # Final save
    metadata["images"] = updated_images
    save_metadata(metadata, metadata_file)
    
    logger.info("=== Person Filtering Complete ===")
    logger.info(f"Total processed: {len(images)}")
    logger.info(f"Approved: {approved_count}")
    logger.info(f"Rejected and moved: {rejected_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter raw crawled images for person existence")
    parser.add_argument("--raw-dir", type=str, default=str(DATA_RAW), help="Raw data directory")
    parser.add_argument("--rejected-dir", type=str, default=str(DATA_REJECTED), help="Rejected data directory")
    args = parser.parse_args()
    
    filter_images(Path(args.raw_dir), Path(args.rejected_dir))
