import hashlib
import pickle

def memoize(func):
    def wrapper(*args, **kwargs):
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