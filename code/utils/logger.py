import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
LOG_DIR.mkdir(exist_ok=True)

_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

_file_handler = logging.FileHandler(LOG_DIR / "pipeline.log", encoding="utf-8")
_file_handler.setFormatter(_formatter)

_stream_handler = logging.StreamHandler()
_stream_handler.setFormatter(_formatter)

def get_logger(name: str = "orchestrate") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        logger.addHandler(_file_handler)
        logger.addHandler(_stream_handler)
    return logger

logger = get_logger("orchestrate")