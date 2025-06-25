from datetime import datetime, timedelta

class JobExpiring_Cleanup:
    def __init__(self, expiry_minutes=30):
        self.jobs = []
        self.expiry_minutes = expiry_minutes

    def add_job(self, job_id, user_id):
        job = {
            'job_id': job_id,
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.jobs.append(job)
        print(f"[INFO] Job {job_id} added at {job['created_at']} by User {user_id}.")

    def get_waiting_time(self, job):
        return datetime.now() - job['created_at']

    def is_expired(self, job):
        return self.get_waiting_time(job) > timedelta(minutes=self.expiry_minutes)

    def notify_expiry(self, job):
        print(f"[NOTIFY] Job {job['job_id']} for User {job['user_id']} has expired.")

    def remove_expired_jobs(self):

        remaining_jobs = []
        for job in self.jobs:
            if self.is_expired(job):
                self.notify_expiry(job)
            else:
                remaining_jobs.append(job)
        self.jobs = remaining_jobs

    def show_status(self):
        print(f"[STATUS] Current Jobs ({len(self.jobs)}):")
        for job in self.jobs:
            wait_time = self.get_waiting_time(job)
            print(f"  - Job {job['job_id']} | User {job['user_id']} | Waiting {wait_time}")


if __name__ == "__main__":
    system = JobExpiring_Cleanup(expiry_minutes=0.05)

    system.add_job(1, 101)
    system.add_job(2, 102)

    import time
    time.sleep(5)

    system.remove_expired_jobs()
    system.show_status()
