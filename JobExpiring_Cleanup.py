from typing import List

class PrintJob:
    def __init__(self, job_id):
        self.job_id = job_id
        self.status = None

    def is_expired(self, current_time):
        return True

class JobStatus:
    EXPIRED = "Expired"

class CircularQueue:
    def __init__(self):
        self.jobs = []

    def get_all_jobs(self):
        return self.jobs

    def remove_job(self, job_id):
        for job in self.jobs:
            if job.job_id == job_id:
                self.jobs.remove(job)
                return True
        return False

class JobExpiryHandler:
    """Handles job expiration and cleanup"""

    def __init__(self, default_expiry: float = 30.0):
        self.default_expiry = default_expiry
        self.expired_jobs: List[PrintJob] = []

    def remove_expired_jobs(self, queue: 'CircularQueue', current_time: float) -> int:
        """Remove jobs that have exceeded their expiry time"""
        expired_count = 0
        expired_job_ids = []

        all_jobs = queue.get_all_jobs()

        for job in all_jobs:
            if job.is_expired(current_time):
                expired_job_ids.append(job.job_id)

        for job_id in expired_job_ids:
            if queue.remove_job(job_id):
                for job in all_jobs + self.expired_jobs:
                    if job.job_id == job_id:
                        job.status = JobStatus.EXPIRED
                        self.expired_jobs.append(job)
                        break
                expired_count += 1

        return expired_count

    def notify_job_expiry(self, expired_job: 'PrintJob') -> None:
        print(f"Job {expired_job.job_id} has expired.")

# Example usage
if __name__ == "__main__":
    q = CircularQueue()
    q.jobs = [PrintJob("job1"), PrintJob("job2")]
    handler = JobExpiryHandler()
    expired = handler.remove_expired_jobs(q, current_time=999.0)
    print(f"Expired jobs removed: {expired}")
