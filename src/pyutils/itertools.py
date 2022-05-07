import numpy as np
from itertools import islice
from itertools import chain

def np_chunks(x, chunk_size):
    chunk_count = len(x)//chunk_size
    n = chunk_count * chunk_size
    shape = x.shape[1:]
    return x[:n].reshape(chunk_count, chunk_size, *shape)

def chunks(x, n):
    # return slices of lists
    if hasattr(x, '__len__'):
        for i in range(0, len(x), n):
            yield x[i:i+n]
    else:
        # return sub-generators of generators
        i = iter(x)
        for e in i:
            yield chain([e], islice(i, n-1))