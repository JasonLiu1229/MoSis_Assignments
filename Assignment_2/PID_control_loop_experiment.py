#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   __main__.py -F CBD -e PIDCLBlock -sSrgv PID_control_loop.drawio -E delta=0.1

from PID_control_loop import *
from pyCBD.simulator import Simulator

DELTA_T = 0.1

cbd = PIDCLBlock("PIDCLBlock")

# Run the Simulation
sim = Simulator(cbd)
sim.setDeltaT(DELTA_T)
sim.run(10)

# TODO: Process Your Simulation Results