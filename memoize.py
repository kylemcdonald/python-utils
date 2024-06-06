import hashlib
import pickle
import inspect

def memoize(func):
    is_method = 'self' in inspect.getfullargspec(func).args
    def wrapper(*args, **kwargs):
        if is_method:
            args = args[1:] # ignore self
        h = hashlib.md5(str(args).encode()).hexdigest()
        fn = f"cache/{func.__name__}_{h}.pkl"
        try:
            with open(fn, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            result = func(*args, **kwargs)
            with open(fn, 'wb') as f:
                pickle.dump(result, f)
            return result
    return wrapper