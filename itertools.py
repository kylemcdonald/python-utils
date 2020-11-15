import numpy as np

def np_chunks(x, chunk_size):
    chunk_count = len(x)//chunk_size
    n = chunk_count * chunk_size
    shape = x.shape[1:]
    return x[:n].reshape(chunk_count, chunk_size, *shape)

def chunks(x, n):
    for i in range(0, len(x), n):
        yield x[i:i+n]