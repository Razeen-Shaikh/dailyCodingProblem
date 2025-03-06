"""
    Implement a job scheduler which takes in a function f and an integer n, and calls f after n milliseconds.

    Args:
        f (function): The function to be called after n milliseconds.
        n (int): The number of milliseconds to wait before calling f.

    Returns:
        None
"""

import threading
import time



def job_scheduler(f, n):
    """Schedules function f to run after n milliseconds."""
    timer = threading.Timer(n / 1000, f)
    timer.start()

def example_function():
    print(f"Function executed at {time.time()}")

print(f"Scheduling function at {time.time()}")
job_scheduler(example_function, 2000)
