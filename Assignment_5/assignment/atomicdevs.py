
### EDIT THIS FILE ###

from pypdevs.DEVS import AtomicDEVS
from environment import *
import random
import dataclasses
import queue

@dataclasses.dataclass
class QueueState:
    queues: dict[int, queue.Queue]
    
    def __init__(self, ship_sizes):
        self.queues = {size: queue.Queue() for size in ship_sizes}

class Queue(AtomicDEVS):
    def __init__(self, ship_sizes):
        super().__init__("Queue")
        
        self.ship_sizes = ship_sizes
        self.state = QueueState(ship_sizes=ship_sizes)

    # def extTransition(self, inputs):
    #     pass
    
    # def timeAdvance(self):
    #     pass
    
    # def outputFnc(self):
    #     pass
    
    # def intTransition(self):
    #     pass

PRIORITIZE_BIGGER_SHIPS = 0
PRIORITIZE_SMALLER_SHIPS = 1

@dataclasses.dataclass
class LoadBalancerState:
    lock_capacities: list[int] 
    current_lock: int  # Index of the lock for round-robin strategy
    priority: int  # Priority type (e.g., PRIORITIZE_BIGGER_SHIPS or PRIORITIZE_SMALLER_SHIPS)

    def __init__(self, lock_capacities, priority):
        self.lock_capacities = lock_capacities[:]
        self.current_lock = 0
        self.priority = priority

class RoundRobinLoadBalancer(AtomicDEVS):
    def __init__(self,
        lock_capacities=[3,2], # two locks of capacities 3 and 2.
        priority=PRIORITIZE_BIGGER_SHIPS,
    ):
        super().__init__("RoundRobinLoadBalancer")
        self.state = LoadBalancerState(lock_capacities=lock_capacities, priority=priority)

    # def extTransition(self, inputs):
    #     pass
    
    # def timeAdvance(self):
    #     pass
    
    # def outputFnc(self):
    #     pass
    
    # def intTransition(self):
    #     pass

class FillErUpLoadBalancer(AtomicDEVS):
    def __init__(self,
        lock_capacities=[3,2], # two locks of capacities 3 and 2.
        priority=PRIORITIZE_BIGGER_SHIPS,
    ):
        super().__init__("FillErUpLoadBalancer")
        self.state = LoadBalancerState(lock_capacities=lock_capacities, priority=priority)

    # def extTransition(self, inputs):
    #     pass
    
    # def timeAdvance(self):
    #     pass
    
    # def outputFnc(self):
    #     pass
    
    # def intTransition(self):
    #     pass

@dataclasses.dataclass
class LockState:
    remaining_capacity: int
    
    def __init__(self, capacity):
        self.remaining_capacity = capacity

class Lock(AtomicDEVS):
    def __init__(self,
        capacity=2, # lock capacity (2 means: 2 ships of size 1 will fit, or 1 ship of size 2)
        max_wait_duration=60.0, 
        passthrough_duration=60.0*15.0, # how long does it take for the lock to let a ship pass through it
    ):
        super().__init__("Lock")
        self.state = LockState(capacity=capacity)
        self.max_wait_duration = max_wait_duration
        self.passthrough_duration = passthrough_duration

    # def extTransition(self, inputs):
    #     pass
    
    # def timeAdvance(self):
    #     pass
    
    # def outputFnc(self):
    #     pass
    
    # def intTransition(self):
    #     pass


### EDIT THIS FILE ###
