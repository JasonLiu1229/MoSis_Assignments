#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   packages/DrawioConvert/__main__.py -F CBD -sSrgv drawio_files/Backwards_Euler.drawio -e BackwardsEuler -d drawio_converter_files/ 

from pyCBD.Core import *
from pyCBD.lib.std import *

DELTA_T = 0.1

class BackwardsEuler(CBD):
    def __init__(self, block_name):
        super().__init__(block_name, input_ports=['IC', 'IN'], output_ports=['OUT'])

        # Create the Blocks
        self.addBlock(DelayBlock("JwoozNrwMrIAiXocNwRg-151"))
        self.addBlock(DeltaTBlock("JwoozNrwMrIAiXocNwRg-158"))
        self.addBlock(DelayBlock("JwoozNrwMrIAiXocNwRg-160"))
        self.addBlock(ConstantBlock("JwoozNrwMrIAiXocNwRg-165", value=(0)))
        self.addBlock(ProductBlock("JwoozNrwMrIAiXocNwRg-170", numberOfInputs=(2)))
        self.addBlock(AdderBlock("JwoozNrwMrIAiXocNwRg-176", numberOfInputs=(2)))

        # Create the Connections
        self.addConnection("IC", "JwoozNrwMrIAiXocNwRg-151", input_port_name='IC')
        self.addConnection("IN", "JwoozNrwMrIAiXocNwRg-160", input_port_name='IN1')
        self.addConnection("JwoozNrwMrIAiXocNwRg-165", "JwoozNrwMrIAiXocNwRg-160", output_port_name='OUT1', input_port_name='IC')
        self.addConnection("JwoozNrwMrIAiXocNwRg-160", "JwoozNrwMrIAiXocNwRg-170", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("JwoozNrwMrIAiXocNwRg-158", "JwoozNrwMrIAiXocNwRg-170", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("JwoozNrwMrIAiXocNwRg-170", "JwoozNrwMrIAiXocNwRg-176", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("JwoozNrwMrIAiXocNwRg-151", "JwoozNrwMrIAiXocNwRg-176", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("JwoozNrwMrIAiXocNwRg-176", "JwoozNrwMrIAiXocNwRg-151", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("JwoozNrwMrIAiXocNwRg-176", "OUT", output_port_name='OUT1')


