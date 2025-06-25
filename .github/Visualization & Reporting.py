class QueueVisualizer:

    @staticmethod
    def show_status(queue: CircularQueue, current_time: float, stats: Dict[str, int]):

        print(f"\n{'=' * 60}")
        print(f"PRINT QUEUE STATUS - Time: {current_time:.1f}s")
        print(f"{'=' * 60}")

        jobs = queue.get_all_jobs()
        if not jobs:
            print("Queue is EMPTY")
        else:
            print(f"Queue Size: {len(jobs)}/{queue._capacity}")
            print(f"{'Rank':<4} {'User-Job':<15} {'Priority':<8} {'Waiting':<8} {'Expires In':<10}")
            print("-" * 60)

            for i, job in enumerate(jobs, 1):
                expires_in = max(0, job.expiry_time - job.waiting_time)
                print(f"{i:<4} {job.user_id}-{job.job_id:<15} "
                      f"{job.priority:<8} {job.waiting_time:.1f}s{'':<3} {expires_in:.1f}s")

        print(f"\nSTATISTICS:")
        print(f"  Submitted: {stats['total_submitted']}")
        print(f"  Printed: {stats['total_printed']}")
        print(f"  Expired: {stats['total_expired']}")
        print(f"  Jobs Aged: {stats['jobs_aged']}")
        print(f"  Simultaneous Submissions: {stats['simultaneous_submissions']}")
        print(f"{'=' * 60}\n")

    @staticmethod
    def get_job_info(queue: CircularQueue, job_id: str,
                     completed_jobs: List[PrintJob], expired_jobs: List[PrintJob]) -> Optional[Dict[str, Any]]:

        for job in queue.get_all_jobs():
            if job.job_id == job_id:
                return {
                    'id': job.job_id,
                    'user_id': job.user_id,
                    'status': job.status.value,
                    'current_priority': job.priority,
                    'original_priority': job.original_priority,
                    'content': job.content,
                    'submission_time': job.submission_time,
                    'waiting_time': job.waiting_time,
                    'expires_in': max(0, job.expiry_time - job.waiting_time),
                    'times_aged': job.original_priority - job.priority
                }

        for job in completed_jobs:
            if job.job_id == job_id:
                return {
                    'id': job.job_id,
                    'user_id': job.user_id,
                    'status': job.status.value,
                    'final_priority': job.priority,
                    'original_priority': job.original_priority,
                    'content': job.content,
                    'total_waiting_time': job.waiting_time
                }

        for job in expired_jobs:
            if job.job_id == job_id:
                return {
                    'id': job.job_id,
                    'user_id': job.user_id,
                    'status': job.status.value,
                    'reason': 'Expired due to timeout'
                }

        return None

class PrintQueueManager:

    def __init__(self, capacity: int = 100, aging_interval: float = 5.0,
                 aging_increment: int = 1, default_expiry: float = 30.0):

        self.queue = CircularQueue(capacity)
        self.priority_system = PriorityAgingSystem(aging_interval, aging_increment)
        self.expiry_handler = JobExpiryHandler(default_expiry)
        self.concurrent_handler = ConcurrentSubmissionHandler()
        self.time_manager = TimeManager()
        self.visualizer = QueueVisualizer()

        self.completed_jobs: List[PrintJob] = []
        self.event_log: List[str] = []
        self.stats = {
            'total_submitted': 0,
            'total_printed': 0,
            'total_expired': 0,
            'jobs_aged': 0,
            'simultaneous_submissions': 0
        }

    def enqueue_job(self, user_id: str, job_id: str, priority: int,
                    content: str = "Document", expiry_time: Optional[float] = None) -> bool:

        for job in self.queue.get_all_jobs():
            if job.job_id == job_id:
                self._log_event(f"ERROR: Job {job_id} already exists!")
                return False


        job = PrintJob(
            user_id=user_id,
            job_id=job_id,
            priority=priority,
            content=content,
            expiry_time=expiry_time or self.expiry_handler.default_expiry
        )


        if self.queue.enqueue_job(job):
            self.stats['total_submitted'] += 1
            self._log_event(f"Job {user_id}-{job_id} added (Priority: {priority})")
            return True
        else:
            self._log_event(f"ERROR: Queue full! Cannot add job {user_id}-{job_id}")
            return False

    def print_job(self) -> Optional[PrintJob]:

        job = self.queue.dequeue_job()
        if job:
            job.status = JobStatus.COMPLETED
            job.update_waiting_time(self.time_manager.current_time)
            self.completed_jobs.append(job)
            self.stats['total_printed'] += 1
            self._log_event(f"PRINTED: {job.user_id}-{job.job_id} "
                            f"(Priority: {job.priority}, Waited: {job.waiting_time:.1f}s)")
            return job
        else:
            self._log_event("No jobs to print - queue is empty!")
            return None

    def handle_simultaneous_submissions(self, job_specs: List[Tuple[str, str, int, str]]) -> Dict[str, bool]:

        self.stats['simultaneous_submissions'] += 1
        self._log_event(f"SIMULTANEOUS SUBMISSION: {len(job_specs)} jobs")

        results = self.concurrent_handler.handle_simultaneous_submissions(self.queue, job_specs)
        successful = sum(1 for success in results.values() if success)
        self._log_event(f"Simultaneous submission completed: {successful}/{len(job_specs)} successful")

        return results

    def tick(self, time_increment: float = 1.0):
        current_time = self.time_manager.tick(time_increment)


        self.time_manager.update_waiting_times(self.queue)


        aged_count = self.priority_system.apply_priority_aging(self.queue, current_time)
        self.stats['jobs_aged'] += aged_count


        expired_count = self.expiry_handler.remove_expired_jobs(self.queue, current_time)
        self.stats['total_expired'] += expired_count

    def show_status(self):

        self.visualizer.show_status(
            self.queue,
            self.time_manager.current_time,
            self.stats
        )

    def get_job_info(self, job_id: str) -> Optional[Dict[str, Any]]:

        return self.visualizer.get_job_info(
            self.queue,
            job_id,
            self.completed_jobs,
            self.expiry_handler.expired_jobs
        )

    def _log_event(self, message: str):

        timestamp = f"[{self.time_manager.current_time:.1f}s]"
        log_entry = f"{timestamp} {message}"
        self.event_log.append(log_entry)
        print(log_entry)


def run_simulation():

    print("PRINT QUEUE SIMULATOR")
    print("=" * 50)

    pq = PrintQueueManager(
        capacity=20,
        aging_interval=3.0,
        aging_increment=1,
        default_expiry=15.0
    )


    print("\n1. Adding initial jobs...")
    pq.enqueue_job("Alice", "doc1", 5, "Important Report")
    pq.enqueue_job("Bob", "photo1", 3, "Family Photos")
    pq.enqueue_job("Charlie", "thesis", 1, "PhD Thesis")
    pq.enqueue_job("Diana", "memo", 4, "Office Memo")

    pq.show_status()


    print("\n2. Printing highest priority job...")
    pq.print_job()
    pq.show_status()


    print("\n3. Time passing (aging will occur)...")
    pq.tick(4.0)
    pq.show_status()


    print("\n4. Simultaneous job submissions...")
    simultaneous_jobs = [
        ("Eve", "urgent1", 2, "Urgent Document"),
        ("Frank", "report2", 3, "Monthly Report"),
        ("Grace", "invoice", 4, "Client Invoice"),
        ("Henry", "proposal", 1, "Project Proposal")
    ]

    pq.handle_simultaneous_submissions(simultaneous_jobs)
    pq.show_status()


    print("\n5. More time passing (some jobs may expire)...")
    pq.tick(8.0)
    pq.show_status()


    print("\n6. Processing multiple jobs...")
    for _ in range(3):
        job = pq.print_job()
        if job:
            time.sleep(0.5)

    pq.show_status()


    print("\n7. Letting remaining jobs expire...")
    pq.tick(10.0)
    pq.show_status()

    print("\n8. Job information lookup...")
    job_info = pq.get_job_info("thesis")
    if job_info:
        print(f"Job 'thesis' info: {job_info}")

    print("\nSimulation completed!")
    print(f"Final statistics: {pq.stats}")


if __name__ == "__main__":
    run_simulation()