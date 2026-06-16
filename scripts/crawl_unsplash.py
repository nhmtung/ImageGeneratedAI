"""Unsplash crawler script for Phase 1.

Downloads fashion/portrait images using the Unsplash search API.
"""

import argparse
import os
import random
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm
from src import utils as utils
from src.utils import ensure_dir, load_metadata, save_metadata, setup_logger
from src.config import DATA_RAW, DEFAULT_CRAWL_LIMIT, DATA_RAW_NSFW, NSFW_KEYWORDS

load_dotenv()
logger = setup_logger("crawl_unsplash")

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



def crawl_unsplash(limit: int, output_dir: Path, keywords: list = None) -> None:
    """Download images from Unsplash API.

    Args:
        limit: Max images to request per keyword query.
        output_dir: Path to write raw downloads to.
        keywords: Optional list of keywords to crawl.
    """
    api_key = os.getenv("UNSPLASH_KEY")
    if not api_key:
        logger.error("UNSPLASH_KEY is not defined in the environment. Please configure .env.")
        return

    ensure_dir(output_dir)
    metadata_file = output_dir / "metadata.json"
    metadata = load_metadata(metadata_file)
    existing_urls = {item["url"] for item in metadata.get("images", [])}

    headers = {"Authorization": f"Client-ID {api_key}"}
    search_url = "https://api.unsplash.com/search/photos"

    # Use provided keywords or fall back to DEFAULT_KEYWORDS
    search_keywords = keywords if keywords is not None else DEFAULT_KEYWORDS
    for query in search_keywords:
        logger.info(f"Querying Unsplash for: '{query}'")
        query_slug = query.replace(" ", "_")
        
        # Unsplash pagination limit is 30 per page
        per_page = min(30, limit)
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
                res = utils.retry_request(search_url, headers=headers, params=params)
                data = res.json()
                results = data.get("results", [])
                if not results:
                    break
                
                for idx, item in enumerate(tqdm(results, desc=f"Page {page}")):
                    if count >= limit:
                        break
                    
                    # We download 'regular' size (1080px wide) as it strikes a good quality/weight balance
                    img_url = item.get("urls", {}).get("regular")
                    if not img_url or img_url in existing_urls:
                        continue
                    
                    filename = f"unsplash_{query_slug}_{page:02d}_{idx:02d}.jpg"
                    filepath = output_dir / filename
                    
                    # Download the image file
                    img_res = utils.retry_request(img_url)
                    with open(filepath, "wb") as f:
                        f.write(img_res.content)
                    
                    # Add item to metadata JSON
                    metadata["images"].append({
                        "filename": filename,
                        "source": "Unsplash",
                        "url": img_url,
                        "resolution": [item.get("width"), item.get("height")],
                        "has_person": None,  # Evaluated later by filter_person.py
                        "crawled_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    })
                    existing_urls.add(img_url)
                    save_metadata(metadata, metadata_file)
                    
                    count += 1
                    # Polite sleep delay to protect API limits
                    time.sleep(random.uniform(1.0, 2.5))
                    
            except Exception as e:
                logger.error(f"Error occurred crawling query '{query}' page {page}: {e}")
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unsplash portrait fashion crawler")
    parser.add_argument("--limit", type=int, default=DEFAULT_CRAWL_LIMIT, help="Max images per query")
    parser.add_argument("--output-dir", type=str, default=str(DATA_RAW), help="Output directory")
    parser.add_argument("--include-nsfw", action="store_true", help="Include NSFW image crawling")
    args = parser.parse_args()

    # Regular (safe) crawl
    crawl_unsplash(args.limit, Path(args.output_dir))

    # NSFW crawl if requested
    if args.include_nsfw:
        from src.config import DATA_RAW_NSFW
        crawl_unsplash(args.limit, DATA_RAW_NSFW, keywords=NSFW_KEYWORDS)
