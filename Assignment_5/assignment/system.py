### EDIT THIS FILE ###

from pypdevs.DEVS import CoupledDEVS
from atomicdevs import *

STRATEGY_ROUND_ROBIN = 0
STRATEGY_FILL_ER_UP = 1


class LockQueueingSystem(CoupledDEVS):
    def __init__(
        self,
        # See runner.py for an explanation of these parameters!!
        seed,
        gen_num,
        gen_rate,
        gen_types,
        load_balancer_strategy,
        lock_capacities,
        priority,
        max_wait_duration,
        passthrough_duration,
    ):
        super().__init__("LockQueueingSystem")

        # Instantiate sub-models with the right parameters, and add them to the CoupledDEVS:

        generator = self.addSubModel(
            Generator(
                seed=seed,  # random seed
                lambd=gen_rate,
                gen_types=gen_types,
                gen_num=gen_num,
            )
        )

        queue = self.addSubModel(
            Queue(
                ship_sizes=set(
                    gen_types
                ),  # the queue only needs to know the different ship sizes (and create a FIFO queue for each)
            )
        )

        if load_balancer_strategy == STRATEGY_ROUND_ROBIN:
            LoadBalancer = RoundRobinLoadBalancer
        elif load_balancer_strategy == STRATEGY_FILL_ER_UP:
            LoadBalancer = FillErUpLoadBalancer

        load_balancer = self.addSubModel(
            LoadBalancer(
                lock_capacities=lock_capacities,
                priority=priority,
            )
        )

        locks = [
            self.addSubModel(
                Lock(
                    capacity=lock_capacity,
                    max_wait_duration=max_wait_duration,
                    passthrough_duration=passthrough_duration,
                )
            )
            for lock_capacity in lock_capacities
        ]

        sink = self.addSubModel(Sink())

        # Don't forget to connect the input/output ports of the different sub-models:
        #   for instance:
        #     self.connectPorts(generator.out_ship, queue.in_ship)
        #     ...

        self.connectPorts(generator.out_ship, queue.in_ship)
        self.connectPorts(queue.out_ship, load_balancer.in_ship)
        self.connectPorts(queue.out_available, load_balancer.in_ships_available)
        self.connectPorts(load_balancer.out_request, queue.in_request)

        for i in range(len(locks)):
            self.connectPorts(load_balancer.out_locks[i], locks[i].in_ship)
            self.connectPorts(locks[i].out_open, load_balancer.in_locks[i])
            self.connectPorts(locks[i].out_ships, sink.in_ships)

        # Our runner.py script needs access to the 'sink'-state after completing the simulation:
        self.sink = sink


### EDIT THIS FILE ###
