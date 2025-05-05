import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Scraping settings
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3

# Storage settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/ipl_matches.db")
CACHE_DIR = BASE_DIR / "data" / "cache"
CACHE_EXPIRY = 3600  # 1 hour in seconds

# Output settings
OUTPUT_FORMATS = ["csv", "json", "parquet"]
DEFAULT_OUTPUT = "csv"