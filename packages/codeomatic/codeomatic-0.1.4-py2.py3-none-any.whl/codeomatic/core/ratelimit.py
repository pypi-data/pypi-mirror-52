import time
import threading
from functools import wraps


def rate_limited(time_period: float = 1.0, max_calls: int = 3):
    """
    Rate limiting decorator inspired by
    https://gist.github.com/gregburek/1441055

    :param time_period: Time period in seconds
    :param max_calls: Number of allowed calls per time period
    :return: decorator
    """
    lock = threading.Lock()
    min_interval = time_period / max_calls

    def decorate(func):
        last_time_called = time.perf_counter()

        @wraps(func)
        def rate_limited_function(*args, **kwargs):
            lock.acquire()
            nonlocal last_time_called
            elapsed = time.perf_counter() - last_time_called
            left_to_wait = min_interval - elapsed

            if left_to_wait > 0:
                time.sleep(left_to_wait)

            try:
                ret = func(*args, **kwargs)
            finally:
                last_time_called = time.perf_counter()
                lock.release()
            return ret

        return rate_limited_function

    return decorate


def block(time_period: float = 1.0, max_calls: int = 3):
    """
    Halt for a period of time to make sure we don't execute some function
    more often than we're allowed.

    :param time_period: Time period in seconds
    :param max_calls: Number of allowed calls per time period
    :return: None
    """
    func = rate_limited(time_period, max_calls)(lambda: None)
    return func()
