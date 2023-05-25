import logging
from logging.handlers import TimedRotatingFileHandler
import datetime

def setup_logger():
    logger = logging.getLogger(__name__)
    for handler in logger.handlers:
        logger.removeHandler(handler)
    logger.setLevel(logging.DEBUG)
    
    log_filename = f"application_log_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
    file_handler = TimedRotatingFileHandler(log_filename, when='midnight', interval=1)
    file_handler.setLevel(logging.DEBUG)
    log_format  = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_format )
    logger.addHandler(file_handler)

    return logger