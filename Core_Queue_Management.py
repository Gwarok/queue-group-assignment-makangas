from enum import Enum
import threading
import time
from typing import Optional, List, Tuple, Dict, Any
from dataclasses import dataclass, field

# shared
class JobStatus(Enum):
    PENDING = "pending"
    PRINTING = "printing"
    COMPLETED = "completed"
    EXPIRED = "expired"


@dataclass(order=True)
class PrintJob:

    user_id: str
    job_id: str
    priority: int
    content: str = "Document"
    submission_time: float = field(default_factory=time.time)
    waiting_time: float = 0.0
    original_priority: int = field(init=False)
    last_aged: float = field(default_factory=time.time)
    status: JobStatus = JobStatus.PENDING
    expiry_time: float = 30.0

    def post_init_(self):
        self.original_priority = self.priority

    def update_waiting_time(self, current_time: float):
        self.waiting_time = current_time - self.submission_time

    def is_expired(self, current_time: float) -> bool:
        return (current_time - self.submission_time) >= self.expiry_time

    def can_be_aged(self, current_time: float, aging_interval: float) -> bool:
        return (current_time - self.last_aged) >= aging_interval

    def apply_aging(self, current_time: float, aging_increment: int = 1) -> bool:
        if self.priority > 1:  # Prevent priority from going below 1
            self.priority -= aging_increment
            self.last_aged = current_time
            return True
        return False

# Core queue management
class CircularQueue:
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.data: List[Optional[PrintJob]] = [None] * capacity
        self.front = 0
        self.size = 0
        self.lock = threading.RLock()
        self.total_jobs_submitted = 0
        self.total_jobs_printed = 0

    def len(self) -> int:
        return self.size

    def is_empty(self) -> bool:
        return self.size == 0

    def is_full(self) -> bool:
        return self.size == self.capacity

    def enqueue_job(self, job: PrintJob) -> bool:
        with self.lock:
            if self.is_full():
                return False

            insert_pos = self.find_insert_position(job)
            self.insert_at_position(job, insert_pos)

            self.size += 1
            self.total_jobs_submitted += 1
            return True

    def find_insert_position(self, new_job: PrintJob) -> int:
        if self.size == 0:
            return 0

        for i in range(self.size):
            current_index = (self.front + i) % self.capacity
            current_job = self.data[current_index]

            if current_job is not None and new_job < current_job:
                return i

        return self.size

    def insert_at_position(self, job: PrintJob, position: int):
        if position == self.size:
            back_pos = (self.front + self.size) % self.capacity
            self.data[back_pos] = job
        else:
            for i in range(self.size, position, -1):
                old_pos = (self.front + i - 1) % self.capacity
                new_pos = (self.front + i) % self.capacity
                self.data[new_pos] = self.data[old_pos]

            insert_pos = (self.front + position) % self.capacity
            self.data[insert_pos] = job

    def dequeue_job(self) -> Optional[PrintJob]:
        with self.lock:
            if self.is_empty():
                return None

            job = self.data[self.front]
            self.data[self.front] = None
            self.front = (self.front + 1) % self.capacity
            self.size -= 1
            self.total_jobs_printed += 1

            return job

    def peek_job(self) -> Optional[PrintJob]:
        # Return the highest priority job without removing it
        with self.lock:
            if self.is_empty():
                return None
            return self.data[self.front]

    def get_all_jobs(self) -> List[PrintJob]:
        with self.lock:
            jobs: List[PrintJob] = []
            for i in range(self.size):
                index = (self.front + i) % self.capacity
                job = self.data[index]
                if job is not None:
                    jobs.append(job)
            return jobs

    def remove_job(self, job_id: str) -> bool:
        with self.lock:
            for i in range(self.size):
                index = (self.front + i) % self.capacity
                job = self.data[index]
                if job is not None and job.job_id == job_id:
                    for j in range(i, self.size - 1):
                        current_index = (self.front + j) % self.capacity
                        next_index = (self.front + j + 1) % self.capacity
                        self.data[current_index] = self.data[next_index]

                    last_index = (self.front + self.size - 1) % self.capacity
                    self.data[last_index] = None
                    self.size -= 1
                    return True
            return False