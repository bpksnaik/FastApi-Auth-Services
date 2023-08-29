import logging

# basic logger...
log_format = "%(asctime)s - %(levelname)s - %(message)s"
log_level = logging.INFO
logging.basicConfig(filename="./log/log_data.txt", format=log_format, level=log_level)
logger = logging.getLogger(__name__)
