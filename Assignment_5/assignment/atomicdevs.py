
### EDIT THIS FILE ###

from pypdevs.DEVS import AtomicDEVS
from environment import *
import random
import dataclasses


@dataclasses.dataclass
class QueueState:
    queues: dict[int, list]
    request: bool
    pop_index: int
    new_size_available: bool
    
    def __init__(self, ship_sizes):
        self.queues = {size: [] for size in ship_sizes}
        self.request = False
        self.pop_index = 0
        self.new_size_available = False


class Queue(AtomicDEVS):
    def __init__(self, ship_sizes):
        super().__init__("Queue")
        
        self.ship_sizes = ship_sizes
        self.state = QueueState(ship_sizes=ship_sizes)
        
        self.in_ship = self.addInPort("in_queue")
        self.in_request = self.addInPort("in_request")

        self.out_ship = self.addOutPort("out_queue")
        self.out_available = self.addOutPort("out_available")

    def extTransition(self, inputs):
        # ship arrival
        if self.in_ship in inputs:
            ship = inputs[self.in_ship]
            if not self.state.queues[ship.size]:
                self.state.new_size_available = True
            self.state.queues[ship.size].append(ship)

        # ship request from loadbalancer
        if self.in_request in inputs:
            self.state.request = True
            self.state.pop_index = inputs[self.in_request]

        return self.state
    
    def timeAdvance(self):
        return 0 if self.state.request or self.state.new_size_available else float("inf")
    
    def outputFnc(self):
        output = {}
        # notify new ship availabilities
        if self.state.new_size_available:
            # output all ship sizes with non-empty queue
            output[self.out_available] = [i for i, q in self.state.queues.items() if not q]

        # output ship
        if self.state.request:
            output[self.out_ship] = self.state.queues[self.state.pop_index][0]
        
        return output
    
    def intTransition(self):
        self.state.new_size_available = False

        if self.state.request:
            self.state.queues[self.state.pop_index].pop(0)
            self.state.request = False

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


class LoadBalancer(AtomicDEVS):
    def __init__(self,
        name="LoadBalancer",
        lock_capacities=[3,2], # two locks of capacities 3 and 2.
        priority=PRIORITIZE_BIGGER_SHIPS,
    ):
        super().__init__(name)
        self.state = LoadBalancerState(lock_capacities=lock_capacities, priority=priority)
        
        self.in_ship = self.addInPort("in_event") # ship inbound
        self.in_ships_available = self.addInPort("in_available") # which sizes of ships are in the queue
        
        self.out_request = self.addOutPort("out_request_ship") # send a request for a ship of a size
        self.out_locks = [self.addOutPort(f"out_event_to_lock{i}" for i in range(len(lock_capacities)))] # list of all locks


class RoundRobinLoadBalancer(LoadBalancer):
    def __init__(self,
        lock_capacities=[3,2], # two locks of capacities 3 and 2.
        priority=PRIORITIZE_BIGGER_SHIPS,
    ):
        super().__init__("RoundRobinLoadBalancer", lock_capacities, priority)

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


class FillErUpLoadBalancer(LoadBalancer):
    def __init__(self,
        lock_capacities=[3,2], # two locks of capacities 3 and 2.
        priority=PRIORITIZE_BIGGER_SHIPS,
    ):
        super().__init__("FillErUpLoadBalancer", lock_capacities, priority)


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
