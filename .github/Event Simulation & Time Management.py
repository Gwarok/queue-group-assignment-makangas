class TimeManager:


    def __init__(self):
        self.current_time = 0.0
        self.time_lock = threading.RLock()

    def tick(self, time_increment: float = 1.0) -> float:

        with self.time_lock:
            self.current_time += time_increment
            return self.current_time

    def update_waiting_times(self, queue: CircularQueue):

        with self.time_lock:
            for job in queue.get_all_jobs():
                job.update_waiting_time(self.current_time)