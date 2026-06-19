import json
import hashlib
from pathlib import Path
from utils.logger import logger

CACHE_DIR = Path(__file__).resolve().parents[1] / ".cache"
CACHE_DIR.mkdir(exist_ok=True)


def _key(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def get(prompt: str):
    path = CACHE_DIR / f"{_key(prompt)}.json"
    try:
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            logger.info("Cache HIT")
            return data
    except Exception as e:
        logger.warning(f"Cache read error: {e}")
    return None


def set(prompt: str, response):
    path = CACHE_DIR / f"{_key(prompt)}.json"
    try:
        path.write_text(json.dumps(response, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        logger.warning(f"Cache write error: {e}")


def clear():
    for f in CACHE_DIR.glob("*.json"):
        f.unlink()
    logger.info("Cache cleared")