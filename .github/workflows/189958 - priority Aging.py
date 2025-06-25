class PriorityAgingSystem:


    def _init_(self, aging_interval: float = 5.0, aging_increment: int = 1):
        self.aging_interval = aging_interval
        self.aging_increment = aging_increment

    def apply_priority_aging(self, queue: CircularQueue, current_time: float) -> int:

        aged_count = 0
        jobs_to_reorder = []

        for job in queue.get_all_jobs():
            if job.can_be_aged(current_time, self.aging_interval):
                if job.apply_aging(current_time, self.aging_increment):
                    aged_count += 1
                    jobs_to_reorder.append(job)

        if jobs_to_reorder:
            self._reorder_queue(queue)

        return aged_count

    @staticmethod
    def _reorder_queue(queue: CircularQueue):

        all_jobs = queue.get_all_jobs()
        queue._size = 0
        queue._front = 0

        for job in all_jobs:
            queue.enqueue_job(job)

