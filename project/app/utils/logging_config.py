

import logging
import os
from dotenv import load_dotenv

load_dotenv()

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO").upper()

def configure_logger():
    
    logger = logging.getLogger(__name__)
    
    logger.setLevel(LOGGING_LEVEL)
    
    handler = logging.StreamHandler()
    handler.setLevel(LOGGING_LEVEL)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger

logger = configure_logger()
