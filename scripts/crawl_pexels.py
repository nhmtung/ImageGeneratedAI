"""Pexels crawler script for Phase 1.

Downloads fashion/portrait images using the Pexels search API.
"""

import argparse
import os
import random
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm
from src.config import DATA_RAW, DEFAULT_CRAWL_LIMIT
from src.utils import ensure_dir, load_metadata, retry_request, save_metadata, setup_logger

load_dotenv()
logger = setup_logger("crawl_pexels")

# Standard searches targeting Vietnamese and East Asian style portraits
DEFAULT_KEYWORDS = [
    "vietnamese woman fashion",
    "ao dai",
    "vietnam girl portrait",
    "vietnamese dress",
    "asian woman fashion",
    "korean woman outfit",
    "japanese woman portrait",
    "chinese dress",
    "woman full body portrait",
    "woman standing pose",
]

def crawl_pexels(limit: int, output_dir: Path) -> None:
    """Download images from Pexels API.

    Args:
        limit: Max images to request per keyword query.
        output_dir: Path to write raw downloads to.
    """
    api_key = os.getenv("PEXELS_KEY")
    if not api_key:
        logger.error("PEXELS_KEY is not defined in the environment. Please configure .env.")
        return

    ensure_dir(output_dir)
    metadata_file = output_dir / "metadata.json"
    metadata = load_metadata(metadata_file)
    existing_urls = {item["url"] for item in metadata.get("images", [])}

    headers = {"Authorization": api_key}
    search_url = "https://api.pexels.com/v1/search"

    for query in DEFAULT_KEYWORDS:
        logger.info(f"Querying Pexels for: '{query}'")
        query_slug = query.replace(" ", "_")
        
        # Pexels supports up to 80 per page
        per_page = min(80, limit)
        pages = (limit + per_page - 1) // per_page
        
        count = 0
        for page in range(1, pages + 1):
            if count >= limit:
                break
            
            params = {
                "query": query,
                "page": page,
                "per_page": per_page,
                "orientation": "portrait"
            }
            
            try:
                # API Call with retry & exponential backoff
                res = retry_request(search_url, headers=headers, params=params)
                data = res.json()
                photos = data.get("photos", [])
                if not photos:
                    break
                
                for idx, photo in enumerate(tqdm(photos, desc=f"Page {page}")):
                    if count >= limit:
                        break
                    
                    # Large size (typically ~940px wide) strikes a good budget/quality balance
                    img_url = photo.get("src", {}).get("large")
                    original_url = photo.get("url")
                    if not img_url or original_url in existing_urls:
                        continue
                    
                    filename = f"pexels_{query_slug}_{page:02d}_{idx:02d}.jpg"
                    filepath = output_dir / filename
                    
                    # Download the image file
                    img_res = retry_request(img_url)
                    with open(filepath, "wb") as f:
                        f.write(img_res.content)
                    
                    # Add item to metadata JSON
                    metadata["images"].append({
                        "filename": filename,
                        "source": "Pexels",
                        "url": original_url,
                        "resolution": [photo.get("width"), photo.get("height")],
                        "has_person": None,  # Evaluated later by filter_person.py
                        "crawled_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    })
                    existing_urls.add(original_url)
                    save_metadata(metadata, metadata_file)
                    
                    count += 1
                    # Polite sleep delay
                    time.sleep(random.uniform(1.0, 2.5))
                    
            except Exception as e:
                logger.error(f"Error occurred crawling query '{query}' page {page}: {e}")
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pexels portrait fashion crawler")
    parser.add_argument("--limit", type=int, default=DEFAULT_CRAWL_LIMIT, help="Max images per query")
    parser.add_argument("--output-dir", type=str, default=str(DATA_RAW), help="Output directory")
    args = parser.parse_args()
    
    crawl_pexels(args.limit, Path(args.output_dir))
