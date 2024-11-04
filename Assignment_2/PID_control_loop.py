#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   __main__.py -F CBD -e PIDCLBlock -sSrgv PID_control_loop.drawio -E delta=0.1

from pyCBD.Core import *
from pyCBD.lib.std import *

DELTA_T = 0.1

class PIDCLBlock(CBD):
    def __init__(self, block_name):
        super().__init__(block_name, input_ports=['x(t)'], output_ports=['u(t)'])

        # Create the Blocks
        self.addBlock(NegatorBlock("DzCg6ToobE1hvCms1og_-4"))
        self.addBlock(AdderBlock("DzCg6ToobE1hvCms1og_-7", numberOfInputs=(2)))
        self.addBlock(ConstantBlock("DzCg6ToobE1hvCms1og_-11", value=(10)))
        self.addBlock(IntegratorBlock("DzCg6ToobE1hvCms1og_-13"))
        self.addBlock(DerivatorBlock("DzCg6ToobE1hvCms1og_-17"))
        self.addBlock(AdderBlock("DzCg6ToobE1hvCms1og_-21", numberOfInputs=(2)))
        self.addBlock(AdderBlock("DzCg6ToobE1hvCms1og_-25", numberOfInputs=(2)))
        self.addBlock(ProductBlock("DzCg6ToobE1hvCms1og_-29", numberOfInputs=(2)))
        self.addBlock(ConstantBlock("K_p", value=(16)))
        self.addBlock(ConstantBlock("K_d", value=(10)))
        self.addBlock(ConstantBlock("K_i", value=(1)))

        # Create the Connections
        self.addConnection("DzCg6ToobE1hvCms1og_-17", "DzCg6ToobE1hvCms1og_-25", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("DzCg6ToobE1hvCms1og_-21", "DzCg6ToobE1hvCms1og_-25", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("DzCg6ToobE1hvCms1og_-13", "DzCg6ToobE1hvCms1og_-21", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("DzCg6ToobE1hvCms1og_-29", "DzCg6ToobE1hvCms1og_-21", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("K_p", "DzCg6ToobE1hvCms1og_-29", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("DzCg6ToobE1hvCms1og_-7", "DzCg6ToobE1hvCms1og_-13", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("DzCg6ToobE1hvCms1og_-7", "DzCg6ToobE1hvCms1og_-29", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("DzCg6ToobE1hvCms1og_-7", "DzCg6ToobE1hvCms1og_-17", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("K_i", "DzCg6ToobE1hvCms1og_-13", output_port_name='OUT1', input_port_name='IC')
        self.addConnection("K_d", "DzCg6ToobE1hvCms1og_-17", output_port_name='OUT1', input_port_name='IC')
        self.addConnection("DzCg6ToobE1hvCms1og_-11", "DzCg6ToobE1hvCms1og_-7", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("DzCg6ToobE1hvCms1og_-4", "DzCg6ToobE1hvCms1og_-7", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("x(t)", "DzCg6ToobE1hvCms1og_-4", input_port_name='IN1')
        self.addConnection("DzCg6ToobE1hvCms1og_-25", "u(t)", output_port_name='OUT1')


