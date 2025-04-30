# logging_utils.py
import logging
import os
from pathlib import Path

def setup_logger(log_name, log_file, level=logging.INFO):
    log_dir = Path(__file__).parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / log_file

    logger = logging.getLogger(log_name)
    logger.setLevel(level)

    # Avoid duplicate handlers
    if not any(isinstance(h, logging.FileHandler) and h.baseFilename == str(log_path) for h in logger.handlers):
        fh = logging.FileHandler(log_path, mode='a')
        fh.setLevel(level)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger
