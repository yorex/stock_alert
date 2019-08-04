import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
loc_app = Flask(__name__)


LEVEL_DEBUG=0
LEVEL_INFO=1
LEVEL_WARN=2
LEVEL_ERROR=3

########### current log level
level=1
#####

#log_path = './logs/web.log'
#handler = RotatingFileHandler(log_path, maxBytes=50000000, backupCount=11)
#formatter = logging.Formatter(
#            "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
#handler.setFormatter(formatter)
#loc_app.logger.addHandler(handler)
#CRITICAL 50, ERROR 40, WARNING 30, INFO 20, DEBUG 10, NOTSET 0
loc_app.logger.setLevel((level+1)*10)


def debug(*kargs):
    if LEVEL_DEBUG < level:
        return
    loc_app.logger.debug(*kargs)
    #print(kargs[0] % kargs[1:])

def info(*kargs):
    if LEVEL_INFO < level:
        return
    loc_app.logger.info(*kargs)

def warn(*kargs):
    if LEVEL_WARN < level:
        return
    loc_app.logger.warn(*kargs)

def error(*kargs):
    if LEVEL_ERROR < level:
        return
    loc_app.logger.error(*kargs)

def debug_print(*kargs):
    if LEVEL_DEBUG < level:
        return
    loc_app.logger.debug(*kargs)
    print(kargs[0] % kargs[1:])


def info_print(*kargs):
    if LEVEL_INFO < level:
        return
    loc_app.logger.info(*kargs)
    print(kargs[0] % kargs[1:])

def warn_print(*kargs):
    if LEVEL_WARN < level:
        return
    loc_app.logger.warn(*kargs)
    print(kargs[0] % kargs[1:])

def error_print(*kargs):
    if LEVEL_ERROR < level:
        return
    loc_app.logger.error(*kargs)
    print(kargs[0] % kargs[1:])


if __name__ == "__main__":
    debug("test debug %s", "log")
    info("test info %s", "log")
    error_print("test info %s", "log")
