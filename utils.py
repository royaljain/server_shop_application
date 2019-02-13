import time
import logging
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def safe_run(func):

    def func_wrapper(*args, **kwargs):

        try:
           return func(*args, **kwargs)

        except Exception as e:
            logging.exception(e)
            return {'status': 'Failure'}
            

    return func_wrapper


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result

    return timed
