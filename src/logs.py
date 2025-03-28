import logging
from logging.handlers import RotatingFileHandler

log_directory = '../logs'
info_logs = f'{log_directory}/info.log'
warning_logs = f'{log_directory}/warning.log'
error_logs = f'{log_directory}/error.log'

max_log_size = 10 * 1024 * 1024 #10 megabytes
backups = 1

def setup_loggers():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create handlers for different log levels
    info_handler = logging.FileHandler(info_logs)
    info_handler.setLevel(logging.INFO)
    info_handler = RotatingFileHandler(info_logs, maxBytes=max_log_size, backupCount=backups)
    info_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    info_handler.addFilter(lambda record: record.levelno == logging.INFO)

    warning_handler = logging.FileHandler(warning_logs)
    warning_handler.setLevel(logging.WARNING)
    warning_handler = RotatingFileHandler(warning_logs, maxBytes=max_log_size, backupCount=backups)
    warning_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    warning_handler.addFilter(lambda record: record.levelno == logging.WARNING)

    error_handler = logging.FileHandler(error_logs)
    error_handler.setLevel(logging.ERROR)
    error_handler = RotatingFileHandler(error_logs, maxBytes=max_log_size, backupCount=backups)
    error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    error_handler.addFilter(lambda record: record.levelno == logging.ERROR)

    # Add the handlers to the root logger
    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(error_handler)

    return logger

logger = setup_loggers()

def create_info_logs(message):
    logger.info(message)
    
    
def create_warning_logs(message):
    logger.warning(message)
    
def create_error_logs(message):
    logger.error(message)

def create_log(level, message):
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.error(message)
    elif level == "error":
        logger.error(message)
    
if __name__ == "__main__":
    # Test logging

    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    
    create_info_logs("This is an info message called by a function.")
    create_warning_logs("This is a warning message called by a function.")
    create_error_logs("This is an error message called by a function.")