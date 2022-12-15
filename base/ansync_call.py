from threading import Thread
def async_call(fn):
    def wrapper(*args, **kwargs):
        th = Thread(target=fn, args=args, kwargs=kwargs)
        th.setDaemon(True)
        th.start()
    return wrapper