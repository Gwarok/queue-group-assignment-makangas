import threading
import time
from datetime import datetime
from collections import deque
from typing import List, Dict, Optional, Tuple


class PrintJob:
    def __init__(self, user_id: str, job_id: str, priority: int, content: str = "Document"):
        self.user_id = user_id
        self.job_id = job_id
        self.priority = priority
        self.content = content
        self.submission_time = time.time()
        self.waiting_time = 0
        self.original_priority = priority

    def __str__(self):
        return f"Job({self.user_id}-{self.job_id}, P:{self.priority}, W:{self.waiting_time}s)"

    def __repr__(self):
        return self.__str__()

def __len__(self):
    return self._size


def is_empty(self):
    return self._size == 0


def is_full(self):
    return self._size == self._capacity


def enqueue_job(self, user_id: str, job_id: str, priority: int, content: str = "Document"):
    with self._lock:
        if self.is_full():
            print(f"Queue is full! Cannot add job {user_id}-{job_id}")
            return False

        # Create new print job
        new_job = PrintJob(user_id, job_id, priority, content)

        # Find correct position based on priority
        insert_pos = self._find_insert_position(new_job)

        # Insert job at the correct position
        self._insert_at_position(new_job, insert_pos)

        self._size += 1
        self.total_jobs_submitted += 1

        print(f"Job {user_id}-{job_id} added with priority {priority}")
        return True


def _find_insert_position(self, new_job: PrintJob) -> int:
    #Find the correct position to insert a job based on priority.
    if self._size == 0:
        return 0

    # Search for the right position (higher priority = lower number = higher precedence)
    for i in range(self._size):
        current_index = (self._front + i) % self._capacity
        current_job = self._data[current_index]

        # Insert before jobs with lower priority or same priority but longer waiting time
        if (new_job.priority < current_job.priority or
                (new_job.priority == current_job.priority and
                 new_job.submission_time < current_job.submission_time)):
            return i

    return self._size  # Insert at the end


def _insert_at_position(self, job: PrintJob, position: int):
    # Insert a job at a specific position in the circular queue
    if position == self._size:
        # Insert at the end
        back_pos = (self._front + self._size) % self._capacity
        self._data[back_pos] = job
    else:
        # Shift elements to make room
        for i in range(self._size, position, -1):
            old_pos = (self._front + i - 1) % self._capacity
            new_pos = (self._front + i) % self._capacity
            self._data[new_pos] = self._data[old_pos]

        # Insert the new job
        insert_pos = (self._front + position) % self._capacity
        self._data[insert_pos] = job


def print_job(self) -> Optional[PrintJob]:
    # Remove and return the highest priority job from the queue.
    with self._lock:
        if self.is_empty():
            print("No jobs to print - queue is empty!!")
            return None

        # Get the job at the front
        job_to_print = self._data[self._front]

        # Clear the position
        self._data[self._front] = None

        # Move front pointer
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        self.total_jobs_printed += 1

        print(f"Printing job: {job_to_print.user_id}-{job_to_print.job_id} "
              f"(Priority: {job_to_print.priority}, Waited: {job_to_print.waiting_time}s)")

        return job_to_print