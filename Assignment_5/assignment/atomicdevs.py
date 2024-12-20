
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
            output[self.out_available] = [i for i, q in self.state.queues.items() if q]

        # output ship
        if self.state.request:
            output[self.out_ship] = self.state.queues[self.state.pop_index][0]
            # Queue is now empty
            if len(self.state.queues[self.state.pop_index]) == 1:
                output[self.out_available] = [i for i, q in self.state.queues.items() if q and (i != self.state.pop_index)]
        
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
    lock_capacities: list[tuple[int, int]] # List of (max capacity, remaining capacity) of the locks
    priority: int  # Priority type (e.g., PRIORITIZE_BIGGER_SHIPS or PRIORITIZE_SMALLER_SHIPS)
    sizes_available: list[int] # Which sizes of ships are available in the queue
    ship: Ship | None # Current ship
    next_lock: int  # Index of lock to send the ship
    send_request: bool # Request a ship from the queue if True
    request_size: int # Size of the ship to request

    def __init__(self, lock_capacities, priority):
        self.lock_capacities = [(i, i) for i in lock_capacities]
        self.priority = priority
        self.sizes_available = []
        self.ship = None
        self.next_lock = 0
        self.send_request = False
        self.request_size = 0


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
        self.in_locks = [self.addInPort(f"in_lock_open{i}") for i in range(len(lock_capacities))] # get notified if a lock is available or not
        
        self.out_request = self.addOutPort("out_request_ship") # send a request for a ship to the queue
        self.out_locks = [self.addOutPort(f"out_event_to_lock{i}") for i in range(len(lock_capacities))] # list of all locks to send ships to

    def process_input(self, inputs):
        """
        Process events from input ports
        """
        # update ships available
        if self.in_ships_available in inputs:
            # sort from small to large
            self.state.sizes_available = sorted(inputs[self.in_ships_available])
        
        # inbound ship
        if self.in_ship in inputs:
            self.state.ship = inputs[self.in_ship]

        # set locks as open or closed
        for i in range(len(self.in_locks)):
            if (lock := self.in_locks[i]) in inputs:
                # open: remaining capacity = max capacity, closed: remaining_capacity = 0
                capacity = self.state.lock_capacities[i][0]
                remaining_capacity = capacity if inputs[lock] else 0
                self.state.lock_capacities[i] = (capacity, remaining_capacity)
                    

class RoundRobinLoadBalancer(LoadBalancer):
    def __init__(self,
        lock_capacities=[3,2], # two locks of capacities 3 and 2.
        priority=PRIORITIZE_BIGGER_SHIPS,
    ):
        super().__init__("RoundRobinLoadBalancer", lock_capacities, priority)

    def round_robin(self):
        # skip locks that do not fit available ships
        i = 0
        while (i < len(self.state.lock_capacities)) and not self.state.send_request:
            lock_index = (self.state.next_lock + i) % len(self.state.lock_capacities)
            current_capacity = self.state.lock_capacities[lock_index][1]

            # if lock is closed
            if current_capacity == 0:
                i += 1
                continue

            # reverse list if bigger ships are prioritized
            available = self.state.sizes_available
            if self.state.priority == PRIORITIZE_BIGGER_SHIPS:
                available = reversed(available)
            
            # check if available ships fit inside of lock
            for size in available:
                if size <= current_capacity:
                    self.state.send_request = True
                    self.state.request_size = size
                    self.state.next_lock = lock_index
                    break
            i += 1

    def extTransition(self, inputs):
        self.process_input(inputs)

        # request next ship
        if (self.state.ship is None) and (self.state.sizes_available):
            self.round_robin()

        return self.state
                
    def timeAdvance(self):
        return 0 if self.state.send_request or self.state.ship else float("inf")
    
    def outputFnc(self):
        output = {}
        if self.state.ship:
            output[self.out_locks[self.state.next_lock]] = self.state.ship
        
        if self.state.send_request:
            output[self.out_request] = self.state.request_size
        
        return output
    
    def intTransition(self):
        if self.state.ship:
            max_capacity, current_capacity = self.state.lock_capacities[self.state.next_lock]
            self.state.lock_capacities[self.state.next_lock] = (max_capacity, current_capacity - self.state.ship.size)
            self.state.next_lock = (self.state.next_lock + 1) % len(self.state.lock_capacities)
            self.state.ship = None
            
        if self.state.sizes_available and not self.state.send_request:
            self.round_robin()
        else:
            self.state.send_request = False
        
        return self.state


class FillErUpLoadBalancer(LoadBalancer):
    def __init__(self,
        lock_capacities=[3,2], # two locks of capacities 3 and 2.
        priority=PRIORITIZE_BIGGER_SHIPS,
    ):
        super().__init__("FillErUpLoadBalancer", lock_capacities, priority)


    def extTransition(self, inputs):
        self.process_input(inputs)

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
    ships: list[Ship]
    passing: bool # True: ships are passing through, False: Lock is waiting for ships, used for output
    
    def __init__(self, capacity):
        self.remaining_capacity = capacity
        self.remaining_time = float("inf")
        self.ships = []
        self.passing = False

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
        self.out_open = self.addOutPort("out_open") # Tell the load balancer that the lock open or closed. True: open, False: closed

    def extTransition(self, inputs):
        self.state.remaining_time -= self.elapsed

        # ship arrival
        if self.in_ship in inputs:
            if self.capacity == self.state.remaining_capacity:
                # The lock is empty
                self.state.remaining_time = self.max_wait_duration
            
            inbound_ship: Ship = inputs[self.in_ship]
            self.state.remaining_capacity -= inbound_ship.size
            self.state.ships.append(inbound_ship)

            # Lock is full, start passthrough
            if self.state.remaining_capacity == 0:
                self.state.remaining_time = self.passthrough_duration
                self.state.passing = True

        return self.state
    
    def timeAdvance(self):
        return self.state.remaining_time

    def outputFnc(self):
        # Passthough finished
        if self.state.passing:
            return {
                self.out_ships: self.state.ships,
                self.out_open: True
            }
        # Force passthrough after max wait duration
        else:
            return {self.out_open: False}

    def intTransition(self):
        # After passthrough, clear lock
        if self.state.passing:
            self.state.ships = []
            self.state.passing = False
            self.state.remaining_time = float("inf")
            self.state.remaining_capacity = self.capacity

        # After max wait duration, start passthrough
        else:
            self.state.passing = True
            self.state.remaining_time = self.passthrough_duration

        return self.state


### EDIT THIS FILE ###
