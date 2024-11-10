#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   packages/DrawioConvert/__main__.py -F CBD -sSrgv drawio_files/g_t.drawio -E delta=0.1 -e g_t -d drawio_converter_files/

from pyCBD.Core import *
from pyCBD.lib.std import *

DELTA_T = 0.1

class g_t(CBD):
    def __init__(self, block_name):
        super().__init__(block_name, input_ports=['t'], output_ports=['g(t)'])

        # Create the Blocks
        self.addBlock(ProductBlock("57yz_Z7oe9A5NPwQm8N_-20", numberOfInputs=(2)))
        self.addBlock(InverterBlock("57yz_Z7oe9A5NPwQm8N_-29"))
        self.addBlock(ProductBlock("57yz_Z7oe9A5NPwQm8N_-33", numberOfInputs=(2)))
        self.addBlock(AdderBlock("lBjsrYSol-ikti7NKIQm-5", numberOfInputs=(2)))
        self.addBlock(AdderBlock("lBjsrYSol-ikti7NKIQm-10", numberOfInputs=(2)))
        self.addBlock(ConstantBlock("lBjsrYSol-ikti7NKIQm-15", value=(2)))
        self.addBlock(ConstantBlock("lBjsrYSol-ikti7NKIQm-17", value=(3)))

        # Create the Connections
        self.addConnection("t", "lBjsrYSol-ikti7NKIQm-5", input_port_name='IN2')
        self.addConnection("t", "lBjsrYSol-ikti7NKIQm-10", input_port_name='IN1')
        self.addConnection("lBjsrYSol-ikti7NKIQm-10", "57yz_Z7oe9A5NPwQm8N_-20", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("lBjsrYSol-ikti7NKIQm-10", "57yz_Z7oe9A5NPwQm8N_-20", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("57yz_Z7oe9A5NPwQm8N_-20", "57yz_Z7oe9A5NPwQm8N_-29", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("57yz_Z7oe9A5NPwQm8N_-29", "57yz_Z7oe9A5NPwQm8N_-33", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("lBjsrYSol-ikti7NKIQm-5", "57yz_Z7oe9A5NPwQm8N_-33", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("57yz_Z7oe9A5NPwQm8N_-33", "g(t)", output_port_name='OUT1')
        self.addConnection("lBjsrYSol-ikti7NKIQm-17", "lBjsrYSol-ikti7NKIQm-10", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("lBjsrYSol-ikti7NKIQm-15", "lBjsrYSol-ikti7NKIQm-5", output_port_name='OUT1', input_port_name='IN1')


