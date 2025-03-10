def add_to_list(value, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(value)
    return my_list


def format_greeting(name, age):
    return f"Hello, my name is {name} and I am {age} years old."


class Counter:
    count = 0 

    def __init__(self):
        Counter.count += 1 

    def get_count(self):
        return Counter.count 


import threading

class SafeCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.count += 1

def worker(counter):
    for _ in range(1000):
        counter.increment()

counter = SafeCounter()
threads = []

for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

def count_occurrences(lst):
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] += 1  # Corrected
        else:
            counts[item] = 1
    return counts
