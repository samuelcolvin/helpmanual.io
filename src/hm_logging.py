import logging

logger = logging.getLogger('helpmanual')


def start_logging():
    fmt = logging.Formatter('%(asctime)s %(name)s: %(message)s', datefmt='%H:%M:%S')

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(fmt)

    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)


