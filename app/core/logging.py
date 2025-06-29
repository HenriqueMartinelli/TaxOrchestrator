import logging

def setup_logger():
    fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt)
    return logging.getLogger("order_service")

logger = setup_logger()
