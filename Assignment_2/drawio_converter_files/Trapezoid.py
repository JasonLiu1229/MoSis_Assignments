#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   packages/DrawioConvert/__main__.py -F CBD -sSrgv drawio_files/Trapezoid.drawio -e Trapezoid -d drawio_converter_files/

from pyCBD.Core import *
from pyCBD.lib.std import *
# For some reason, the GainBlock does not get imported
from pyCBD.lib.std import GainBlock


class Trapezoid(CBD):
    def __init__(self, block_name):
        super().__init__(block_name, input_ports=['IN', 'IC'], output_ports=['OUT'])

        # Create the Blocks
        self.addBlock(DelayBlock("h2C-zFGGvk7dKX5kOmhA-9"))
        self.addBlock(DeltaTBlock("h2C-zFGGvk7dKX5kOmhA-13"))
        self.addBlock(ConstantBlock("h2C-zFGGvk7dKX5kOmhA-15", value=(0)))
        self.addBlock(ProductBlock("h2C-zFGGvk7dKX5kOmhA-17", numberOfInputs=(2)))
        self.addBlock(AdderBlock("h2C-zFGGvk7dKX5kOmhA-22", numberOfInputs=(2)))
        self.addBlock(DelayBlock("h2C-zFGGvk7dKX5kOmhA-53"))
        self.addBlock(AdderBlock("h2C-zFGGvk7dKX5kOmhA-74", numberOfInputs=(2)))
        self.addBlock(GainBlock("h2C-zFGGvk7dKX5kOmhA-82", value=(0.5)))
        self.addBlock(MultiplexerBlock("h2C-zFGGvk7dKX5kOmhA-89"))
        self.addBlock(DelayBlock("h2C-zFGGvk7dKX5kOmhA-96"))
        self.addBlock(AddOneBlock("h2C-zFGGvk7dKX5kOmhA-101"))

        # Create the Connections
        self.addConnection("IC", "h2C-zFGGvk7dKX5kOmhA-9", input_port_name='IC')
        self.addConnection("IN", "h2C-zFGGvk7dKX5kOmhA-53", input_port_name='IN1')
        self.addConnection("IN", "h2C-zFGGvk7dKX5kOmhA-89", input_port_name='IN2')
        self.addConnection("h2C-zFGGvk7dKX5kOmhA-13", "h2C-zFGGvk7dKX5kOmhA-17", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("h2C-zFGGvk7dKX5kOmhA-17", "h2C-zFGGvk7dKX5kOmhA-22", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("h2C-zFGGvk7dKX5kOmhA-9", "h2C-zFGGvk7dKX5kOmhA-22", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("h2C-zFGGvk7dKX5kOmhA-22", "h2C-zFGGvk7dKX5kOmhA-9", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("h2C-zFGGvk7dKX5kOmhA-22", "OUT", output_port_name='OUT1')
        self.addConnection("h2C-zFGGvk7dKX5kOmhA-15", "h2C-zFGGvk7dKX5kOmhA-53", output_port_name='OUT1', input_port_name='IC')
        self.addConnection("h2C-zFGGvk7dKX5kOmhA-15", "h2C-zFGGvk7dKX5kOmhA-89", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("h2C-zFGGvk7dKX5kOmhA-15", "h2C-zFGGvk7dKX5kOmhA-101", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("h2C-zFGGvk7dKX5kOmhA-15", "h2C-zFGGvk7dKX5kOmhA-96", output_port_name='OUT1', input_port_name='IC')
        self.addConnection("h2C-zFGGvk7dKX5kOmhA-74", "h2C-zFGGvk7dKX5kOmhA-82", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("h2C-zFGGvk7dKX5kOmhA-82", "h2C-zFGGvk7dKX5kOmhA-17", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("h2C-zFGGvk7dKX5kOmhA-53", "h2C-zFGGvk7dKX5kOmhA-74", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("h2C-zFGGvk7dKX5kOmhA-96", "h2C-zFGGvk7dKX5kOmhA-89", output_port_name='OUT1', input_port_name='select')
        self.addConnection("h2C-zFGGvk7dKX5kOmhA-101", "h2C-zFGGvk7dKX5kOmhA-96", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("h2C-zFGGvk7dKX5kOmhA-89", "h2C-zFGGvk7dKX5kOmhA-74", output_port_name='OUT1', input_port_name='IN2')


