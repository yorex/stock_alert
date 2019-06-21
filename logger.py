
LEVEL_DEBUG=0
LEVEL_INFO=1
LEVEL_WARN=2
LEVEL_ERROR=3
level=1

def debug(app, *kargs):
    if LEVEL_DEBUG < level:
        return
    if app:
        app.logger.debug(*kargs)
    elif kargs[0]:
        print(kargs[0] % kargs[1:])

def info(app, *kargs):
    if LEVEL_INFO < level:
        return
    if app:
        app.logger.info(*kargs)
    elif kargs[0]:
        print(kargs[0] % kargs[1:])

def warn(app, *kargs):
    if LEVEL_WARN < level:
        return
    if app:
        app.logger.warn(*kargs)
    elif kargs[0]:
        print(kargs[0] % kargs[1:])

def error(app, *kargs):
    if LEVEL_ERROR < level:
        return
    if app:
        app.logger.error(*kargs)
    elif kargs[0]:
        print(kargs[0] % kargs[1:])

if __name__ == "__main__":
    debug(None, "test debug %s", "log")
    info(None, "test info %s", "log")
