#!/usr/bin/env python

"""
python logging done my way

* terse output to stream (console)
* extended output to log file in `.logs` subdirectory

:see: https://docs.python.org/3/library/logging.html

similar project:
https://github.com/fx-kirin/py-stdlogging
"""

import logging
import os

LOG_DIR_BASE = ".logs"


def standard_logging_setup(logger_name, file_name_base=None):
    """
    standard setup for logging
        
    PARAMETERS
    
    logger_name : str
        name of the the logger
    
    file_name_base : str
        Part of the name to store the log file.
        Full name is `f"<PWD>/LOG_DIR_BASE/.{file_name_base}.log"`
        in present working directory.
    """
    file_name_base = file_name_base or logger_name

    log_path = os.path.join(os.getcwd(), LOG_DIR_BASE)
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log_file = os.path.join(log_path, f".{file_name_base}.log")

    # logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    stream_log_handler = logging.StreamHandler()
    logger.addHandler(stream_log_handler)

    # nice output format
    # https://docs.python.org/3/library/logging.html#logrecord-attributes
    stream_log_format = "%(levelname)-.1s"		# only first letter
    stream_log_format += " %(asctime)s"
    stream_log_format += " - "
    stream_log_format += "%(message)s"
    stream_log_handler.setFormatter(
        logging.Formatter(
            stream_log_format,
            datefmt="%a-%H:%M:%S"))
    stream_log_handler.formatter.default_msec_format = "%s.%03d"

    file_log_handler = logging.FileHandler(log_file)
    logger.addHandler(file_log_handler)
    file_log_format = "|%(asctime)s"
    file_log_format += "|%(levelname)s"
    file_log_format += "|%(name)s"
    file_log_format += "|%(module)s"
    file_log_format += "|%(lineno)d"
    file_log_format += "|%(threadName)s"
    file_log_format += "| - "
    file_log_format += "%(message)s"
    file_log_handler.setFormatter(logging.Formatter(file_log_format))
    file_log_handler.formatter.default_msec_format = "%s.%03d"

    return logger
