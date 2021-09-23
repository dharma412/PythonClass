import time
from multiprocessing import Process, Queue, Pool


class ProcessPool(object):
    def __init__(self, func, process_count=5):
        self.process_id = {}
        self.func = func
        self.process_count = process_count
        self.queue = Queue()
        self._create_processes()

    def _create_processes(self):
        for i in range(0, self.process_count):
            process = Process(target=self.func, args=[self.queue])
            process.daemon = True
            process.start()
            self.process_id[process.pid] = process

    def terminate_processes(self):
        if self.process_id:
            for pid, process in self.process_id.items():
                process.terminate()
