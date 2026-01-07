import logging
from app.core.config import settings


def setup_logger():
    logger = logging.getLogger(settings.app_name)
    logger.setLevel(settings.log_level)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = setup_logger()
