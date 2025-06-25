from typing import List

class JobExpiryHandler:
    """Handles job expiration and cleanup"""

    def __init__(self, default_expiry: float = 30.0):
        self.default_expiry = default_expiry
        self.expired_jobs: List['PrintJob'] = []

    def remove_expired_jobs(self, queue: 'CircularQueue', current_time: float, JobStatus=None) -> int:
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
