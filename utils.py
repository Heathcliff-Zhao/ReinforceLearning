from collections import deque
import random


class ReplayMemory:
    def __init__(self, capacity, Transition):
        self.memory = deque([], maxlen=capacity)
        self.Transition = Transition

    def push(self, *args):
        self.memory.append(self.Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)
    
    def fetch(self):
        return self.memory

    def __len__(self):
        return len(self.memory)
    
    def clear(self):
        self.memory.clear()
