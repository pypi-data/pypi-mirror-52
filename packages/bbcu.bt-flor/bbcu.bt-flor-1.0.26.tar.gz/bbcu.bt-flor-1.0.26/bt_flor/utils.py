import logging

logger = logging.getLogger(__name__)


def config_logging(log_file):
    logging_args = {
        "level": logging.DEBUG,
        "filemode": 'w',
        "format": '%(asctime)s %(message)s',
        "datefmt": '%m/%d/%Y %H:%M:%S'
    }
    # set up log file
    if log_file is not None:
        logging_args["filename"] = log_file
    logging.basicConfig(**logging_args)
