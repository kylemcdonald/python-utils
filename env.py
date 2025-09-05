import os

def load_env(key):
    if key in os.environ:
        return os.environ[key]
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                k, v = line.strip().split("=")
                if k == key:
                    return v
    raise KeyError(f"Environment variable {key} not found")