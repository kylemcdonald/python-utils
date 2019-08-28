from time import time
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
                print(f'recent: {recent_fps:0.2f} fps, all: {fps:0.2f} fps, jitter: {jitter:0.4f}s')
                self.last_print = cur_print
                self.recent = []
                clear_output(wait=True)
        else:
            self.start_time = cur_time
        self.total_ticks += 1