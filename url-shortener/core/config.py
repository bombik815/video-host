from pathlib import Path

# D:\_projects\video-host\url-shortener\  - это  BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_URLS_STORAGE_FILEPATH = BASE_DIR / "short-urls.json"
MOVIES_STORAGE_FILEPATH = BASE_DIR / "movies.json"