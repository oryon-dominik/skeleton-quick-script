import functools
import time
import logging
from itertools import chain


log = logging.getLogger('application')


def timer(f_py=None, propagate=False, summary=False, execution_cache=[]):
    assert callable(f_py) or f_py is None
    def _decorator(func):
        """Decorator to time the execution of a function."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            execution_time = None
            # Time it. Execute. Return.
            time_start = time.perf_counter()
            value = func(*args, **kwargs)
            time_end = time.perf_counter()
            execution_time = time_end - time_start
            if propagate:
                log.info(f'Execution time: {execution_time}')
            if summary:
                sum_ = sum(list(chain.from_iterable([et.values() for et in execution_cache])))
                log.info(f'Summed up execution time: {sum_:.3f} s.')
            execution_cache.append({func.__name__: execution_time})
            return value
        return wrapper
    return _decorator(f_py) if callable(f_py) else _decorator
