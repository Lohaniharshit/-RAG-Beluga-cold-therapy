import logging
import os

class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds color to log messages based on their level.
    """
    
    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    GREEN = "\x1b[32;20m"
    RESET = "\x1b[0m"
    
    FORMATS = {
        logging.DEBUG: GREY + '%(asctime)s - %(name)s - %(levelname)s - %(message)s' + RESET,
        logging.INFO: GREEN + '%(asctime)s - %(name)s - %(levelname)s - %(message)s' + RESET,
        logging.WARNING: YELLOW + '%(asctime)s - %(name)s - %(levelname)s - %(message)s' + RESET,
        logging.ERROR: RED + '%(asctime)s - %(name)s - %(levelname)s - %(message)s' + RESET,
        logging.CRITICAL: BOLD_RED + '%(asctime)s - %(name)s - %(levelname)s - %(message)s' + RESET
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logger(name=__name__, level=logging.INFO):
    """
    Sets up a logger with a specific name, level, and format.
    Outputs to console and a file.
    """
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter()) # Use custom colored formatter
    console_handler.setLevel(level)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Add handlers only if they haven't been added to prevent duplicate messages
    if not logger.handlers:
        logger.addHandler(console_handler)

        # Optional: File handler
        # log_dir = "logs"
        # os.makedirs(log_dir, exist_ok=True)
        # file_handler = logging.FileHandler(os.path.join(log_dir, "app.log"))
        # file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')) # Standard formatter for file
        # file_handler.setLevel(logging.DEBUG)
        # logger.addHandler(file_handler)

    return logger

# Example usage (can be removed or modified based on how it's imported)
if __name__ == "__main__":
    logger = setup_logger()
    logger.debug("This is a debug message.")
    logger.info("This is an info message from the logger setup.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
