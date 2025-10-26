import logging

LOGGER_NAME = "resumematch"

logger = logging.getLogger(LOGGER_NAME)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)