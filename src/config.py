from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data directories
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_RAW_NSFW = PROJECT_ROOT / "data" / "raw" / "nsfw"
DATA_REJECTED = PROJECT_ROOT / "data" / "_rejected"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

# Metadata
METADATA_FILE = DATA_RAW / "metadata.json"

# Crawl defaults
DEFAULT_CRAWL_LIMIT = 50
PERSON_CONFIDENCE_THRESHOLD = 0.7

# NSFW keyword list for research crawling
NSFW_KEYWORDS = [
    "lingerie",
    "underwear",
    "boudoir",
    "nude portrait",
    "erotic fashion",
    "sensual women",
    "intimate portrait",
    "sexy outfit",
    "women in bikini",
    "private women portrait",
]
