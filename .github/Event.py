import threading
from typing import List
from time import time as current_time
from circular_queue import CircularQueue
from print_job import PrintJob


class TimeManager:

    def __init__(self, initial_time: float = 0.0):

        self.current_time = initial_time
        self.time_lock = threading.RLock()
        self.last_update_time = current_time()

    def tick(self, time_increment: float = 1.0) -> float:

        with self.time_lock:
            self.current_time += time_increment
            self.last_update_time = current_time()
            return self.current_time

    def update_waiting_times(self, queue: CircularQueue) -> List[PrintJob]:

        with self.time_lock:
            updated_jobs = []
            for job in queue.get_all_jobs():
                job.update_waiting_time(self.current_time)
                updated_jobs.append(job)
            return updated_jobs

    def get_current_time(self) -> float:

        with self.time_lock:
            return self.current_time

    def time_since_last_update(self) -> float:

        with self.time_lock:
            return current_time() - self.last_update_time