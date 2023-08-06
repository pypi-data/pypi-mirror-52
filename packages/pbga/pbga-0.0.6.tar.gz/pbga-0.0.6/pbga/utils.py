import logging

DEFAULT_LOG_FMT = '%(asctime)s %(name)-20s %(levelname)-3s : %(message)s'


def setup_logging(verbosity='info', filename='main.log',
                  log_fmt=DEFAULT_LOG_FMT) -> None:
    """
    Create a basic configuration for the logging library. Set up console and file handler using provided `log_fmt`.
    :param verbosity: verbosity to use, info by default
    :param filename: where to store the log file
    :param log_fmt: format string for logging
    :return: None
    """
    logging.basicConfig(level=logging.DEBUG,
                        format=log_fmt,
                        filename=filename,
                        filemode="w")
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(parse_logging_level(verbosity))
    # set a format which is simpler for console use
    formatter = logging.Formatter(log_fmt)
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)


def parse_logging_level(verbosity: str) -> int:
    """Parse logging verbosity level
    :param verbosity: string representing verbosity, recoginzed strings are {debug, info, warning, error, critical}
    :return: verbosity level as integer
    """
    vu = verbosity.lower()
    if vu == "debug":
        return logging.DEBUG
    elif vu == "info":
        return logging.INFO
    elif vu == "warning":
        return logging.WARNING
    elif vu == "error":
        return logging.ERROR
    elif vu == "critical":
        return logging.CRITICAL
    else:
        print("Unknown logging level {}".format(verbosity))
        return logging.INFO
