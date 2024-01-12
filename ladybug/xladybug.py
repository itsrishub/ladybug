import time
from functools import wraps
import inspect


def debug(func):
    caller_frame = inspect.stack()[1]
    line_number = caller_frame[2]
    if callable(func):
        # before_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print(f'xladybug | Line: {line_number}')
        start = time.time()
        # before_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"xladybug | Calling {func.__name__} with args: {args} and kwargs: {kwargs}")
            result = func(*args, **kwargs)
            print(f"xladybug | {func.__name__} returned: {result}")
            
            return result
        end = time.time()
        # after_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # memory_diff_kb = after_memory - before_memory
        # print(f"Memory usage of {func.__name__}: {memory_diff_kb} KB | {memory_diff_kb/1024} MB")
        print(f"xladybug | Execution time of {func.__name__}: {end - start} seconds")
        return wrapper
    else:
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        try:
            print(f'xladybug | Line: {line_number} | {[var_name for var_name, var_val in callers_local_vars if var_val is func][0]}: {func}')
        except:
            print(f'xladybug | Line: {line_number} | {func}')
