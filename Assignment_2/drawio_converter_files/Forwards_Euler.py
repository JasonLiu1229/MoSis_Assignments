#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   packages/DrawioConvert/__main__.py -F CBD -sSrgv drawio_files/Forwards_Euler.drawio -e ForwardsEuler -d drawio_converter_files/

from pyCBD.Core import *
from pyCBD.lib.std import *


class ForwardsEuler(CBD):
    def __init__(self, block_name):
        super().__init__(block_name, input_ports=['IN', 'IC'], output_ports=['OUT'])

        # Create the Blocks
        self.addBlock(DelayBlock("VJJN_RWPSZKce4CWAGm1-218"))
        self.addBlock(DeltaTBlock("VJJN_RWPSZKce4CWAGm1-222"))
        self.addBlock(ConstantBlock("VJJN_RWPSZKce4CWAGm1-228", value=(0)))
        self.addBlock(ProductBlock("VJJN_RWPSZKce4CWAGm1-231", numberOfInputs=(2)))
        self.addBlock(AdderBlock("VJJN_RWPSZKce4CWAGm1-237", numberOfInputs=(2)))
        self.addBlock(MultiplexerBlock("VJJN_RWPSZKce4CWAGm1-269"))
        self.addBlock(AddOneBlock("VJJN_RWPSZKce4CWAGm1-279"))
        self.addBlock(DelayBlock("VJJN_RWPSZKce4CWAGm1-283"))

        # Create the Connections
        self.addConnection("IC", "VJJN_RWPSZKce4CWAGm1-218", input_port_name='IC')
        self.addConnection("IN", "VJJN_RWPSZKce4CWAGm1-269", input_port_name='IN2')
        self.addConnection("VJJN_RWPSZKce4CWAGm1-222", "VJJN_RWPSZKce4CWAGm1-231", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("VJJN_RWPSZKce4CWAGm1-231", "VJJN_RWPSZKce4CWAGm1-237", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("VJJN_RWPSZKce4CWAGm1-218", "VJJN_RWPSZKce4CWAGm1-237", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("VJJN_RWPSZKce4CWAGm1-237", "VJJN_RWPSZKce4CWAGm1-218", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("VJJN_RWPSZKce4CWAGm1-237", "OUT", output_port_name='OUT1')
        self.addConnection("VJJN_RWPSZKce4CWAGm1-228", "VJJN_RWPSZKce4CWAGm1-269", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("VJJN_RWPSZKce4CWAGm1-228", "VJJN_RWPSZKce4CWAGm1-279", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("VJJN_RWPSZKce4CWAGm1-228", "VJJN_RWPSZKce4CWAGm1-283", output_port_name='OUT1', input_port_name='IC')
        self.addConnection("VJJN_RWPSZKce4CWAGm1-269", "VJJN_RWPSZKce4CWAGm1-231", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("VJJN_RWPSZKce4CWAGm1-279", "VJJN_RWPSZKce4CWAGm1-283", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("VJJN_RWPSZKce4CWAGm1-283", "VJJN_RWPSZKce4CWAGm1-269", output_port_name='OUT1', input_port_name='select')


