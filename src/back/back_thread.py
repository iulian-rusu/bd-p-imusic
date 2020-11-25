import logging
import threading
from queue import Queue
from typing import Callable


class BackThread(threading.Thread):
    """
    Implements a thread that receives tasks in a queue and runs them one-by-one.
    Mainly used for asynchronous database communication.
    """

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.is_running = False
        self.task_queue = Queue()

    def add_task(self, task: Callable):
        self.task_queue.put(task)

    def start(self):
        self.is_running = True
        threading.Thread.start(self)

    def stop(self):
        self.is_running = False

    def run(self):
        logging.info('Backend thread started')
        while self.is_running:
            task = self.task_queue.get()
            task()
        logging.info('Backend thread stopped')
