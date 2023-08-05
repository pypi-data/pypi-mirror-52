import tkinter as tk
import queue
import threading


class WorkerProcess(threading.Thread):

    def __init__(self, queue):
        super(WorkerProcess, self).__init__()
        self.queue = queue

    def run(self):
        raise NotImplementedError('Implement this method in a sub-class')


class Worker(object):

    def __init__(self, ui):
        self.ui = ui
        if not isinstance(self.ui.master, tk.Tk):
            raise RuntimeError('UI master should be of type tk.Tk')
        self.queue = queue.Queue()
        self.process = None

    def start_process(self, process_cls):
        self.process = process_cls(self.queue)
        self.process.start()
        self.check_process_periodically()

    def check_process_periodically(self):
        self.check_queue()
        if self.process.is_alive():
            self.ui.master.after(100, self.check_process_periodically)

    def check_queue(self):
        while self.queue.qsize():
            try:
                message = self.queue.get(0)
                self.ui.on_worker_update(message)
            except queue.Empty:
                pass
