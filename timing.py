from time import time
from time import sleep
import contextlib
import numpy as np
from IPython.display import clear_output
import json
from multiprocessing import Queue
from multiprocessing import Process
from threading import get_ident
import os
import sys

class Ticker():
    def __init__(self, update_rate=1):
        self.total_ticks = 0
        self.start_time = None
        self.last_print = None
        self.recent = []
        self.clear_output = 'ipykernel' in sys.modules
        self.update_rate = update_rate

    def tick(self):
        cur_time = time()
        self.recent.append(cur_time)
        if self.start_time is not None:
            duration = cur_time - self.start_time
            cur_print = int(duration)
            if cur_print != self.last_print and cur_print % self.update_rate == 0:
                fps = self.total_ticks / duration
                denominator = (self.recent[-1] - self.recent[0])
                if denominator > 0:
                    recent_fps = (len(self.recent) - 1) / denominator
                else:
                    recent_fps = 0
                jitter = np.std(self.recent)
                print(f'recent: {recent_fps:0.2f} fps, all: {fps:0.2f} fps, jitter:', format_time(jitter))
                self.last_print = cur_print
                self.recent = []
                if self.clear_output:
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
            return True
        return False

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

class Tracer():
    def __init__(self, fn):
        self.queue = Queue()
        self.pid_names = {}
        self.tid_names = {}

        self.enabled = True
        if fn is None:
            self.enabled = False
            return

        def tracer_loop():
            output = open(fn, 'w')
            output.write('[\n')
            while True:
                entry = self.queue.get()
                line = json.dumps(entry, separators=(',', ':'))
                output.write(line + ',\n')

        self.set_pid_name('Main')
        self.tracer = Process(target=tracer_loop)
        self.tracer.start()

    def set_tid_name(self, name):
        self.tid_names[get_ident()] = name

    def set_pid_name(self, name):
        self.pid_names[os.getpid()] = name

    @contextlib.contextmanager
    def trace(self, name, pid=None, tid=None):
        ts = time()
        yield
        dur = time() - ts
        if not self.enabled:
            return
        ts *= 1000000 # seconds to microseconds
        dur *= 1000000 # seconds to microseconds
        if pid is None:
            pid = os.getpid()
        if pid in self.pid_names:
            pid = self.pid_names[pid]
        if tid is None:
            tid = get_ident()
        if tid in self.tid_names:
            tid = self.tid_names[tid]
        entry = {
            'name': name,
            'ph': 'X',
            'ts': ts,
            'dur': dur,
            'pid': pid,
            'tid': tid
        }
        self.queue.put(entry)