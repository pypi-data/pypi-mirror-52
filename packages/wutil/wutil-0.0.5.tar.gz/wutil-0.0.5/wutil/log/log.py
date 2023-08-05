import colorlog
import logging
import logging.handlers
import os

def get_logger(log_name, log_level=logging.DEBUG):
    """ Get logger.

    Parameters
    ----------
    log_name : ``str``
        name of log file.
    log_level : ``logging log level``
        log level.

    """
    logger = colorlog.getLogger(log_name)
    logger.propagate = False
    logger.setLevel(log_level)

    formatter = colorlog.ColoredFormatter('%(log_color)s[%(asctime)s %(levelname)s %(funcName)30s] %(message)s', datefmt='%Y/%m/%d %H:%M:%S',
					log_colors={
					    'DEBUG':    'cyan',
					    'INFO':     'white',
					    'WARNING':  'yellow',
					    'ERROR':    'red',
					    'CRITICAL': 'red,bg_white',
					})

    stream_handler = colorlog.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)
    logger.addHandler(stream_handler)

    log_fp = os.path.join('logs', log_name + '.log')
    os.makedirs(os.path.dirname(log_fp), exist_ok=True)
    file_handler = logging.handlers.TimedRotatingFileHandler(log_fp, when='midnight')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    logger.addHandler(file_handler)

    return logger
