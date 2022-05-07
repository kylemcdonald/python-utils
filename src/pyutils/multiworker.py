from threading import Thread
from multiprocessing import Process
from multiprocessing import Queue

class MultiWorker:
    def __init__(self, worker_type, job=None, job_loop=None, num_workers=1):
        self.input_queue = Queue()
        self.output_queue = Queue()
        self.workers = []
        if job_loop is None:
            def job_loop(id, input, output, ready):
                ready.put(id)
                while True:
                    task = input.get()
                    if task is None:
                        break
                    result = job(task)
                    output.put(result)
        ready = Queue()
        for i in range(num_workers):
            worker = Process(target=job_loop, args=(i, self.input_queue, self.output_queue, ready))
            worker.start()
            self.workers.append(worker)
        # block until all workers are ready
        for i in range(num_workers):
            ready.get()
    
    def put(self, task):
        self.input_queue.put(task)

    def get(self):
        return self.output_queue.get()

    def join(self):
        for worker in self.workers:
            self.input_queue.put(None)
        for worker in self.workers:
            worker.join()

class MultiThreadWorker(MultiWorker):
    def __init__(self, **kwargs):
        super().__init__(Thread, **kwargs)

class MultiProcessWorker(MultiWorker):
    def __init__(self, **kwargs):
        super().__init__(Process, **kwargs)