import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "aeroshield.log"),
        logging.StreamHandler(),
    ],
)


def get_logger(name: str):
    """Get logger instance."""
    return logging.getLogger(name)
