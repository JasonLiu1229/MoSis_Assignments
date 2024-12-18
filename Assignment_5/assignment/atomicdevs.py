
### EDIT THIS FILE ###

from pypdevs.DEVS import AtomicDEVS
from environment import *
import random
import dataclasses
import queue

@dataclasses.dataclass
class QueueState:
    queues: dict[int, queue.Queue]
    waiting: bool
    
    def __init__(self, ship_sizes):
        self.queues = {size: queue.Queue() for size in ship_sizes}
        self.waiting = False

class Queue(AtomicDEVS):
    def __init__(self, ship_sizes):
        super().__init__("Queue")
        
        self.ship_sizes = ship_sizes
        self.state = QueueState(ship_sizes=ship_sizes)
        
        self.in_ship = self.addInPort("in_queue")
        self.out_ship = self.addOutPort("out_queue")

    def extTransition(self, inputs):
        if self.in_ship in inputs:
            ship = inputs[self.in_ship]
            self.state.queues[ship.size].put(ship)
            self.state.waiting = True
        return self.state
    
    def timeAdvance(self):
        return 0 if self.state.waiting else float("inf")
    
    def outputFnc(self):
        for size, queue in self.state.queues.items():
            if not queue.empty():
                return {self.out_ship: queue.queue[0]}
        return {}
    
    def intTransition(self):
        self.state.waiting = any(not q.empty() for q in self.state.queues.values())
        # pop the first ship from the queue
        for size, queue in self.state.queues.items():
            if not queue.empty():
                queue.get()
                break
        self.state.waiting = any(not q.empty() for q in self.state.queues.values())
        return self.state

PRIORITIZE_BIGGER_SHIPS = 0
PRIORITIZE_SMALLER_SHIPS = 1

@dataclasses.dataclass
class LoadBalancerState:
    lock_capacities: list[tuple[int, list]]  # dict of lock capacities
    current_lock: int  # Index of the lock for round-robin strategy
    priority: int  # Priority type (e.g., PRIORITIZE_BIGGER_SHIPS or PRIORITIZE_SMALLER_SHIPS)

    def __init__(self, lock_capacities, priority):
        self.lock_capacities = [(capacity, []) for capacity in lock_capacities]
        self.current_lock = 0
        self.priority = priority

class RoundRobinLoadBalancer(AtomicDEVS):
    def __init__(self,
        lock_capacities=[3,2], # two locks of capacities 3 and 2.
        priority=PRIORITIZE_BIGGER_SHIPS,
    ):
        super().__init__("RoundRobinLoadBalancer")
        self.state = LoadBalancerState(lock_capacities=lock_capacities, priority=priority)
        
        self.in_ship = self.addInPort("in_event")
        
        self.out_lock1 = self.addOutPort("out_event_to_lock1")
        self.out_lock2 = self.addOutPort("out_event_to_lock2")

    def extTransition(self, inputs):
        # sort based on ship size
        if self.state.priority == PRIORITIZE_BIGGER_SHIPS:
            inputs = sorted(inputs, key=lambda ship: ship.size, reverse=True)
        elif self.state.priority == PRIORITIZE_SMALLER_SHIPS:
            inputs = sorted(inputs, key=lambda ship: ship.size)
        if self.in_ship in inputs:
            ship = inputs[self.in_ship]
            ship_size = ship.size
            for _ in range(len(self.state.lock_capacities)):
                lock_index = self.state.current_lock
                lock_capacity, lock_ships = self.state.lock_capacities[lock_index]
                if lock_capacity >= ship_size:
                    lock_ships.append(ship)
                    self.state.lock_capacities[lock_index] = (lock_capacity, lock_ships)
                    break
                self.state.current_lock = (self.state.current_lock + 1) % len(self.state.lock_capacities)
        return self.state
                
    def timeAdvance(self):
        return 0
    
    def outputFnc(self):
        for i, (lock_capacity, lock_ships) in enumerate(self.state.lock_capacities):
            if lock_ships:
                return {self.out_lock1 if i == 0 else self.out_lock2: lock_ships[0]}
        return {}
    
    def intTransition(self):
        for i, (lock_capacity, lock_ships) in enumerate(self.state.lock_capacities):
            if lock_ships:
                lock_ships.pop(0)
                self.state.lock_capacities[i] = (lock_capacity, lock_ships)
        return self.state

class FillErUpLoadBalancer(AtomicDEVS):
    def __init__(self,
        lock_capacities=[3,2], # two locks of capacities 3 and 2.
        priority=PRIORITIZE_BIGGER_SHIPS,
    ):
        super().__init__("FillErUpLoadBalancer")
        self.state = LoadBalancerState(lock_capacities=lock_capacities, priority=priority)
        
        self.in_ship = self.addInPort("in_event")
        
        self.out_lock1 = self.addOutPort("out_event_to_lock1")
        self.out_lock2 = self.addOutPort("out_event_to_lock2")

    def extTransition(self, inputs):
        if self.in_ship in inputs:
            ship = inputs[self.in_ship]
            ship_size = ship.size
            
            best_fit = None
            for i, (lock_capacity, lock_ships) in enumerate(self.state.lock_capacities):
                if lock_capacity >= ship_size:
                    fit_value = lock_capacity - ship_size
                    if not best_fit or fit_value < best_fit[1]:
                        best_fit = (i, fit_value)
                        
            if best_fit:
                lock_index = best_fit[0]
                lock_capacity, lock_ships = self.state.lock_capacities[lock_index]
                lock_ships.append(ship)
                self.state.lock_capacities[lock_index] = (lock_capacity, lock_ships)
        return self.state
    
    def timeAdvance(self):
        return 0
    
    def outputFnc(self):
        for i, (lock_capacity, lock_ships) in enumerate(self.state.lock_capacities):
            if lock_ships:
                return {self.out_lock1 if i == 0 else self.out_lock2: lock_ships[0]}
        return {}
    
    def intTransition(self):
        return self.state

@dataclasses.dataclass
class LockState:
    remaining_capacity: int
    remaining_time: float
    ships: list
    wait_time: float
    
    def __init__(self, capacity):
        self.remaining_capacity = capacity
        self.remaining_time = float("inf")
        self.ships = []
        self.wait_time = 0

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
        self.capacity = capacity
        
        self.in_ship = self.addInPort("in_lock")
        self.out_ships = self.addOutPort("out_lock")

    def extTransition(self, inputs):
        self.state.remaining_time -= self.elapsed
        
        if self.elapsed >= 60.0:
            if self.state.remaining_time == float("inf"):
                self.state.remaining_time = self.passthrough_duration
            
        if self.in_ship in inputs:
            ship = inputs[self.in_ship]
            if self.state.remaining_capacity >= ship.size:
                self.state.remaining_capacity -= ship.size
                self.state.ships.append(ship)
                self.state.wait_time = self.max_wait_duration
                if len(self.state.remaining_capacity) == 0:
                    self.state.remaining_time = self.passthrough_duration
        return self.state
    
    def timeAdvance(self):
        return self.state.remaining_time

    def outputFnc(self):
        if len(self.state.ships) > 0:
            return {self.out_ships: self.state.ships}
        return {}

    def intTransition(self):
        self.state.remaining_time = float("inf")
        self.state.remaining_capacity = self.capacity
        return self.state


### EDIT THIS FILE ###
