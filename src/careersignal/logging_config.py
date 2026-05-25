from pathlib import Path
import logging


LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "careersignal.log"


def setup_logging():
    """
    Sets up logging for the CareerSignal project.
    """

    LOG_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger("careersignal")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger