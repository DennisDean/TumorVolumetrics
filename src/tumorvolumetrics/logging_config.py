import logging
import json
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone
import os

APP_NAME = "TumorVolumetrics"

#
# JSON Formatter

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": (
                datetime.fromtimestamp(record.created, tz=timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
            ),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # allow structured extra fields: logger.info("msg", extra={"event": "file_loaded"})
        for key, value in record.__dict__.items():
            if key not in log_record and not key.startswith("_"):
                log_record[key] = value

        return json.dumps(log_record)

#
# Create log directory in the user's home folder
#
log_dir = os.path.join(os.path.expanduser("~"), f".{APP_NAME.lower()}")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "tumor_volumetrics.jsonl")

#
# Configure logger
#
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)
logger.propagate = False

# Prevent duplicate handlers if imported repeatedly
if not logger.handlers:

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File handler (rotating)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=2_000_000,    # 2 MB rotation
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(name)s.%(funcName)s:%(lineno)d - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Register handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info("Structured logger initialized")
