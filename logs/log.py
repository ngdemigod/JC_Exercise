import logging, logging.handlers, datetime

# Create custom logger
today = datetime.date.today()
log_file = 'logs/jc_app.log'
logLevel = 'INFO'


def logger(name=None):
    logFormat = logging.Formatter('[%(asctime)s][%(levelname)s] - %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(filename=log_file, mode='a')
    handler.setFormatter(logFormat)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger