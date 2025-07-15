class Queue:
    # Initializing an empty list
    def __init__(self):
        self.items = []

    # We are adding a new item (FI-FO)
    def enqueue(self, item):
        self.items.insert(0, item)

    # Removing items (FI-FO) if empty return none
    def dequeue(self):
        return self.items.pop() if not self.is_empty() else None

    #See if queue is empty then return True otherwise false
    def is_empty(self):
        return len(self.items) == 0


    def display(self):
        
        return self.items.copy()

    def checkout(self):
        if self.is_empty():
            return "No patients to checkout."
        patient = self.dequeue()
        return f"Checked out patient: {patient}"
