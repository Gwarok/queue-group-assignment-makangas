import threading

class PrintQueueManager:
    def __init__(self):
        self.queue = []
        self.current_time = 0
        self.lock = threading.Lock()

    def enqueue_job(self, user_id, job_id, priority, expiry=10):
        job = {
            'job_id': job_id,
            'user_id': user_id,
            'priority': priority,
            'submitted_at': self.current_time,
            'expiry': expiry
        }

        with self.lock:
            self.queue.append(job)
            print(f"[{threading.current_thread().name}] Job {job_id} from User {user_id} added.")

    def apply_priority_aging(self):
        for job in self.queue:
            wait_time = self.current_time - job['submitted_at']
            if wait_time > 0 and wait_time % 2 == 0:
                job['priority'] += 1
                print(f"Job {job['job_id']} aged to priority {job['priority']}.")

    def remove_expired_jobs(self):
        before_count = len(self.queue)
        self.queue = [
            job for job in self.queue
            if (self.current_time - job['submitted_at']) < job['expiry']
        ]
        after_count = len(self.queue)
        expired = before_count - after_count
        if expired > 0:
            print(f"{expired} job(s) expired and removed from the queue.")

    def handle_simultaneous_submissions(self, jobs):
        threads = []

        for user_id, job_id, priority in jobs:
            thread = threading.Thread(
                target=self.enqueue_job,
                args=(user_id, job_id, priority),
                name=f"Thread-{job_id}"
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def print_job(self):
        if not self.queue:
            print("No jobs to print.")
            return

        self.queue.sort(key=lambda job: (-job['priority'], job['submitted_at']))
        job = self.queue.pop(0)
        print(f"Printed Job {job['job_id']} from User {job['user_id']} with priority {job['priority']}.")

    def tick(self):
        self.current_time += 1
        print(f"\n[Tick {self.current_time}]")

        self.apply_priority_aging()
        self.remove_expired_jobs()
        self.show_status()

    def show_status(self):
        if not self.queue:
            print("Queue is empty.")
        else:
            print("Current Queue Status:")
            for job in sorted(self.queue, key=lambda j: (-j['priority'], j['submitted_at'])):
                wait_time = self.current_time - job['submitted_at']
                print(f"  Job {job['job_id']} | User: {job['user_id']} | Priority: {job['priority']} | Wait: {wait_time}")
