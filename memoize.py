import hashlib
import pickle
import inspect
import os

def memoize(func):
    is_method = 'self' in inspect.getfullargspec(func).args
    def wrapper(*args, **kwargs):
        fn = os.path.join("cache", func.__name__)
        args_to_hash = ""
        if len(args) > 0:
            args_to_hash += str(args[1:] if is_method else args)
        if len(kwargs) > 0:
            args_to_hash += str(kwargs)
        if len(args_to_hash) > 0:
            fn += "_" + hashlib.md5(str(args_to_hash).encode()).hexdigest()
        fn += ".pkl"
        try:
            os.makedirs('cache', exist_ok=True)
            with open(fn, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            result = func(*args, **kwargs)
            with open(fn, 'wb') as f:
                pickle.dump(result, f)
            return result
    return wrapper