import collections
import itertools

def dict_to_iterators(x):
    if isinstance(x, dict):
        return itertools.cycle([dict_to_iterators(x[e]) for e in sorted(x.keys())])
    else:
        return itertools.cycle(x)
    
def deep_default_dict(n):
    if n == 1:
        return collections.defaultdict(list)
    else:
        return collections.defaultdict(lambda: deep_default_dict(n-1))
    
def append_deep_default_dict(d, keys, value):
    cur = d
    for key in keys:
        cur = cur[key]
    cur.append(value)
    
def build_stratified(values, selected=None):
    x = deep_default_dict(len(values))
    for i, keys in enumerate(zip(*values)):
        if selected is None or i in selected:
            append_deep_default_dict(x, keys, i)
    return dict_to_iterators(x)

def next_recursive(x):
    if isinstance(x, collections.Iterable):
        return next_recursive(next(x))
    else:
        return x