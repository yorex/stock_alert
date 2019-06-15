def debug(app, *kargs, **kwargs):
    if app:
        app.logger.debug(*kargs, **kwargs)
    else:
        print(*kargs, **kwargs)

def info(app, *kargs, **kwargs):
    if app:
        app.logger.info(*kargs, **kwargs)
    else:
        print(*kargs, **kwargs)


def warn(app, *kargs, **kwargs):
    if app:
        app.logger.warn(*kargs, **kwargs)
    else:
        print(*kargs, **kwargs)

def error(app, *kargs, **kwargs):
    if app:
        app.logger.error(*kargs, **kwargs)
    else:
        print(*kargs, **kwargs)
