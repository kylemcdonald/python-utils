from time import time
from time import sleep
import contextlib
import numpy as np
from IPython.display import clear_output

class Ticker():
    def __init__(self):
        self.total_ticks = 0
        self.start_time = None
        self.last_print = None
        self.recent = []

    def tick(self):
        cur_time = time()
        self.recent.append(cur_time)
        if self.start_time is not None:
            duration = cur_time - self.start_time
            cur_print = int(duration)
            if cur_print != self.last_print:
                fps = self.total_ticks / duration
                recent_fps = (len(self.recent) - 1) / (self.recent[-1] - self.recent[0])
                jitter = np.std(self.recent)
                print(f'recent: {recent_fps:0.2f} fps, all: {fps:0.2f} fps, jitter:', format_time(jitter))
                self.last_print = cur_print
                self.recent = []
                clear_output(wait=True)
        else:
            self.start_time = cur_time
        self.total_ticks += 1

class Profiler():
    def __init__(self, name):
        self.timing = {}
        self.last_print = None
        self.name = name
        
    @contextlib.contextmanager
    def profile(self, name):
        start = time()
        yield
        elapsed = time() - start
        if name in self.timing:
            self.timing[name][0] += elapsed
            self.timing[name][1] += 1
        else:
            self.timing[name] = [elapsed, 1]
        
    def print(self):
        cur = int(time())
        if cur != self.last_print:
            parts = []
            for name in sorted(self.timing):
                elapsed, count = self.timing[name]
                average = format_time(elapsed / count)
                parts.append(f'{name}: {average}')
            print(self.name + ': ' + ', '.join(parts))
            self.last_print = cur
            self.timing = {}

def format_time(seconds):
    if seconds < 1/1e5:
        return f'{seconds*1e6:0.1f}us'
    if seconds < 1/1e4:
        return f'{seconds*1e6:0.0f}us'
    if seconds < 1/1e2:
        return f'{seconds*1e3:0.1f}ms'
    if seconds < 1/1e1:
        return f'{seconds*1e3:0.0f}ms'
    else:
        return f'{seconds:0.1f}s'