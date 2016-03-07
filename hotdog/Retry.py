import time


def Retry(func, timeout=30):
    def inner(*args, **kwargs):
        start = time.time()
        while True:
            try:
                ret = func(*args, **kwargs)
                return ret
            except:
                if time.time() - start > timeout:
                    raise
    return inner