import logging


# Create a custom logger
logger = logging.getLogger(__name__)

# Create handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.WARNING)

# Create formatter and add it to handler
c_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
c_handler.setFormatter(c_format)

# Add handlers to the logger
logger.addHandler(c_handler)
