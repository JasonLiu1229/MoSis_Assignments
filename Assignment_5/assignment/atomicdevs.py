
### EDIT THIS FILE ###

from pypdevs.DEVS import AtomicDEVS
from environment import *
import random
import dataclasses

class Queue(AtomicDEVS):
    def __init__(self, ship_sizes):
        super().__init__("Queue")
        # self.state = QueueState(...)

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

class RoundRobinLoadBalancer(AtomicDEVS):
    def __init__(self,
        lock_capacities=[3,2], # two locks of capacities 3 and 2.
        priority=PRIORITIZE_BIGGER_SHIPS,
    ):
        super().__init__("RoundRobinLoadBalancer")
        # self.state = LoadBalancerState(...)

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
        # self.state = LoadBalancerState(...)

    # def extTransition(self, inputs):
    #     pass
    
    # def timeAdvance(self):
    #     pass
    
    # def outputFnc(self):
    #     pass
    
    # def intTransition(self):
    #     pass

class Lock(AtomicDEVS):
    def __init__(self,
        capacity=2, # lock capacity (2 means: 2 ships of size 1 will fit, or 1 ship of size 2)
        max_wait_duration=60.0, 
        passthrough_duration=60.0*15.0, # how long does it take for the lock to let a ship pass through it
    ):
        super().__init__("Lock")
        # self.state = LockState(...)

    # def extTransition(self, inputs):
    #     pass
    
    # def timeAdvance(self):
    #     pass
    
    # def outputFnc(self):
    #     pass
    
    # def intTransition(self):
    #     pass


### EDIT THIS FILE ###
