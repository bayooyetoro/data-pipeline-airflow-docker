import logging
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent.parent /"logs/etl_runs.log"

def get_logger(name: str) -> logging.Logger:
    """Logs the ETL runs in the terminal (could be changed to file from the Handler)

        Parameters: 
        name(str): name of the current module, mostly __name__

        Returns:
        logger Object: prints to the terminal or logged to specify files
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(message)s")

        handler = logging.FileHandler(LOG_FILE)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
