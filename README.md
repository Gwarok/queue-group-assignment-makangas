[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/dssR7pGm)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=19803849&assignment_repo_type=AssignmentRepo)
# QUEUE-GROUP-ASSIGNMENT

# PRINTING QUEUE SIMULATION

## Group ASSIGNMENT

This assignment is designed to be quite a fun and engaging challenge that requires teamwork, communication, and collaboration. You will work together to build an advanced print queue simulator that models a real-world printing system with multiple users, priorities, aging, and concurrency.

This project is perfect for groups of **5 to 6 members**. Each member will take ownership of a specific module or feature, and together you will integrate your parts into a fully functioning system.

---

## Project Overview

Your team will develop a **Print Queue Simulator** that supports:

- **Multiple users submitting print jobs concurrently**
- **Job priorities and priority aging** (jobs increase priority the longer they wait)
- **Job expiry** (jobs removed if they wait too long)
- **Simultaneous job submissions**
- **Visual snapshots of the queue state after each event**
- **Robust concurrency handling and synchronization**
- **Extensible design for future features**

---

## FEATURES
### ANY MEMBER CAN TAKE UP ANY MODULE
### 1. Core Queue Management (Module Owner: Member 1)
- Implement the circular queue data structure with fixed capacity.
- Support enqueue, dequeue, and status operations.
- Manage job metadata: user ID, job ID, priority, waiting time.

### 2. Priority & Aging System (Module Owner: Member 2)
- Implement priority-based ordering of jobs.
- Add priority aging: increment job priority after a configurable aging interval.
- Handle tie-breaking by waiting time.

### 3. Job Expiry & Cleanup (Module Owner: Member 3)
- Track waiting times for all jobs.
- Automatically remove expired jobs after a configured expiry time.
- Notify the system and users when jobs expire.

### 4. Concurrent Job Submission Handling (Module Owner: Member 4)
- Support simultaneous job submissions (`send_simultaneous` event).
- Ensure thread-safe enqueue operations.
- Handle race conditions and synchronization.

### 5. Event Simulation & Time Management (Module Owner: Member 5)
- Implement the `tick` event to simulate time passing.
- Update waiting times and apply aging and expiry logic.
- Manage event sequencing and system state updates.

### 6. Visualization & Reporting (Module Owner: Member 6)
- Create clear, user-friendly visual snapshots of the queue state after each event.
- Format output to show job details in print order.
- Optionally, design a simple GUI or web interface (extra credit).

---
## What Each Team Member Should Do

- **Each member picks a module** (like priority handling, job expiry, concurrency, etc.).
- Inside the shared class, **implement your module as a function**. For example:  
  - `def enqueue_job(self, user_id, job_id, priority):`  
  - `def apply_priority_aging(self):`  
  - `def remove_expired_jobs(self):`  
  - `def handle_simultaneous_submissions(self, jobs):`  
  - `def print_job(self):`  
  - `def tick(self):`  
  - `def show_status(self):`

- Make sure your function does **only what it’s supposed to do**

 #### The main program will create one instance of your shared class, like:  
- pq_manager = PrintQueueManager()

  - Then, for each event it reads, it will call the right function on that object:  
  - pq_manager.enqueue_job(user_id, job_id, priority)
  - pq_manager.tick()
  - pq_manager.print_job()
  - pq_manager.show_status()
___
## COLLABORATION

### GitHub Classroom Setup

- The assignment will be distributed via **GitHub Classroom** under the repository named **QUEUE-Assignment**.
- Each group can have **up to 6 members**.
- You will receive a link to accept the assignment: ```` https://classroom.github.com/a/u6FSW6lE````
- Upon acceptance, you will **choose a group name** and specify it.
- Group names will appear in the roster; members select their desired group.
- Groups cannot exceed 6 members.

### Git Branching

- After the group is formed, members will **split the work by module** as outlined above.
- Each member should create a **branch** named using the format:  
  `regno-ft-moduleName`  
  For example: `123456-ft-dequeue`
- Members will work independently on their branches, unless debugging, of which there a should be clear commit messages denoting so.
- Once a module is complete and tested, the branch owner will **merge** their branch into the main branch.
- Regular communication and code reviews are encouraged to ensure smooth integration.

---

## Submission Requirements

### What to Submit

- A **GitHub repository** named **QUEUE-Assignment** with all source code, 
- A **README.md, named submission.md** describing:
  - Group name and member list.
  - Brief description of each member’s module and contributions.
  - Instructions on how to run the code. e.g run main.py
- Clear **commit history** showing individual contributions.
- Branches named as per the branching strategy.
- A **final merged main branch** with a fully working, integrated code.
---

## Note Better

This assignment should foster working as a team, planning your work, and integrating your efforts into a project. Use your group meetings wisely, assign tasks clearly, and help each other accordingly.

---

*If you have any questions or need clarifications, please reach out to:*
```
 bgithenya@strathmore.edu
