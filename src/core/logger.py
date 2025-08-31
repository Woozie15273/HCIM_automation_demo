import logging
from pathlib import Path

def setup_logger(name: str, log_file_name: str = "app.log", level=logging.INFO, enable_log: bool = False) -> logging.Logger:
    """
    Sets up a logger with optional file logging.

    Parameters:
    - name (str): Name of the logger.
    - log_file_name (str): Name of the log file.
    - level (int): Logging level.
    - enable_log (bool): If True, enables file logging.

    Returns:
    - logging.Logger: Configured logger instance.
    """
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate stream handlers
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    # Optional file logging
    if enable_log and not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        try:
            log_path = Path.cwd() / log_file_name
            file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.info(f"File logging enabled. Writing to: {log_path}")
        except Exception as e:
            logger.error(f"Failed to set up file logging: {e}")

    logger.propagate = False
    return logger
