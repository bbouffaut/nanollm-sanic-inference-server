import logging

from src.utils.constants import LOGGING_LEVEL

# Create a logger
logger = logging.getLogger(__name__)
logging_level = LOGGING_LEVEL

# Set the logging level
if logging_level is not None and logging_level.lower() == 'debug':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# Create a console handler and set its logging level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and add it to the console handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)