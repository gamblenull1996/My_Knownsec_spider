# -*- coding:utf-8 -*-
import logging


def logging_config(log, logfile, loglevel):
    # log = logging.getLogger('spider')
    LEVELS = {
        1: logging.CRITICAL,
        2: logging.ERROR,
        3: logging.WARNING,
        4: logging.INFO,
        5: logging.DEBUG
    }
    level = LEVELS[loglevel]
    formatter = logging.Formatter(
        '%(asctime)s %(name)s %(threadName)s [line:%(lineno)d] %(levelname)s %(message)s'
    )
    fileHandler = logging.FileHandler(logfile)
    fileHandler.setFormatter(formatter)
    log.addHandler(fileHandler)
    log.setLevel(LEVELS.get(loglevel))
