import logging

def get_logger() -> logging.Logger: 
    """Create and return a configured logger for the sentiment analyzer."""
    logger = logging.getLogger("sentiment_analyzer")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

logger = get_logger()