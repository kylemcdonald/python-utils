import hashlib
import pickle
import inspect
import os

def memoize(func):
    is_method = 'self' in inspect.getfullargspec(func).args    
    def wrapper(*args, **kwargs):
        args_to_hash = args[1:] if is_method else args
        h = hashlib.md5(str(args_to_hash).encode()).hexdigest()        
        fn = f"cache/{func.__name__}_{h}.pkl"
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