from multiprocessing import Pool, cpu_count
import time
from datetime import datetime, timedelta
import sys

try:
    from IPython.display import clear_output
except ModuleNotFoundError:
    def clear_output(*args, **kwargs):
        pass

def progress(itr, total=None, update_interval=1, clear=True):
    if total is None and hasattr(itr, '__len__'):
        total = len(itr)
        if total == 0:
            return
    if total:
        print(f'0/{total} 0s 0/s')
    else:
        print('0 0s 0/s')
    start_time = None
    last_time = None
    for i, x in enumerate(itr):
        cur_time = time.time()
        if start_time is None:
            start_time = cur_time
            last_time = cur_time
        yield x
        if cur_time - last_time > update_interval:
            duration = cur_time - start_time
            speed = (i + 1) / duration
            duration_str = timedelta(seconds=round(duration))
            if clear:
                clear_output(wait=True)
            if total:
                duration_total = duration * total / (i + 1)
                duration_remaining = duration_total - duration
                duration_remaining_str = timedelta(seconds=round(duration_remaining))
                pct = 100. * (i + 1) / total
                print(f'{pct:.2f}% {i+1}/{total} {duration_str}<{duration_remaining_str} {speed:.2f}/s')
            else:
                print(f'{i+1} {duration_str} {speed:.2f}/s')
            last_time = cur_time
    
    duration = time.time() - start_time
    speed = (i + 1) / duration
    duration_str = timedelta(seconds=round(duration))
    if clear:
        clear_output(wait=True)
    print(f'{i+1} {duration_str} {speed:.2f}/s')
        
class job_wrapper(object):
    def __init__(self, job):
        self.job = job
    def __call__(self, args):
        i, task = args
        return i, self.job(task)
    
def progress_parallel(job, tasks, total=None, processes=None, **kwargs):
    if processes == 1:
        return [job(task) for task in progress(tasks)]
    
    results = []
    if total is None and hasattr(tasks, '__len__'):
        total = len(tasks)
    if processes is None:
        processes = cpu_count()
    try:
        with Pool(processes) as pool:
            results = list(progress(pool.imap_unordered(job_wrapper(job), enumerate(tasks)),
                                    total=total, **kwargs))
            results.sort()
            return [x for i,x in results]
    except KeyboardInterrupt:
        pass

from joblib import Parallel, delayed
def progress_parallel_joblib(job, tasks, total=None, processes=None, backend=None):
    if total is None and hasattr(tasks, '__len__'):
        total = len(tasks)
    if processes is None:
        processes = -1

    try:
        results = Parallel(n_jobs=processes)(delayed(job)(task) for task in progress(tasks))
        return results
    except KeyboardInterrupt:
        pass