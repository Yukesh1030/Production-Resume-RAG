import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


# ============================================================
# LOG DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)


LOG_FILE = LOG_DIR / "app.log"


# ============================================================
# FORMAT
# ============================================================

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ============================================================
# FILE HANDLER
# ============================================================

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8"
)


file_handler.setLevel(
    logging.INFO
)


file_handler.setFormatter(
    logging.Formatter(
        LOG_FORMAT,
        datefmt=DATE_FORMAT
    )
)


# ============================================================
# CONSOLE HANDLER
# ============================================================

console_handler = logging.StreamHandler()

console_handler.setLevel(
    logging.INFO
)

console_handler.setFormatter(
    logging.Formatter(
        LOG_FORMAT,
        datefmt=DATE_FORMAT
    )
)


# ============================================================
# APPLICATION LOGGER
# ============================================================

logger = logging.getLogger(
    "production_resume_rag"
)


logger.setLevel(
    logging.INFO
)


logger.propagate = False


# Prevent duplicate handlers
if not logger.handlers:

    logger.addHandler(
        file_handler
    )

    logger.addHandler(
        console_handler
    )