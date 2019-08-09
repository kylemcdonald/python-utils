import os
import fnmatch

def list_directories(directory):
    for f in os.listdir(directory):
        joined = os.path.join(directory, f)
        if os.path.isdir(joined):
            yield joined

def list_all_files(directory, extensions=None, exclude_prefixes=('__', '.')):
    for root, dirnames, filenames in os.walk(directory):
        filenames = [f for f in filenames if not f.startswith(exclude_prefixes)]
        dirnames[:] = [d for d in dirnames if not d.startswith(exclude_prefixes)]
        for filename in filenames:
            base, ext = os.path.splitext(filename)
            joined = os.path.join(root, filename)
            if extensions is None or ext.lower() in extensions:
                yield joined