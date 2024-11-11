from drawio_converter_files.g_t import g_t
from drawio_converter_files.Backwards_Euler import BackwardsEuler
from drawio_converter_files.Forwards_Euler import ForwardsEuler
from drawio_converter_files.Trapezoid import Trapezoid
from pyCBD.simulator import Simulator
from pyCBD.Core import *
from pyCBD.lib.std import *


class IntegrationTest(CBD):
    def __init__(self, name="IT", integration=BackwardsEuler("integration")):
        CBD.__init__(self, name, input_ports=[], output_ports=["OUT"])
        # integration = BackwardsEuler("integration")
        # integration = ForwardsEuler("integration")
        # integration = Trapezoid("integration")
        gt = g_t("g_t")
        clock = TimeBlock("time")
        ic = ConstantBlock("ic", value=(0))
        self.addBlock(gt)
        self.addBlock(integration)
        self.addBlock(clock)
        self.addBlock(ic)
        self.addConnection("time", "g_t", input_port_name="t", output_port_name="OUT1")
        self.addConnection("g_t", "integration", input_port_name="IN", output_port_name="g(t)")
        # testing with cosine instead of g(t)
        # self.addBlock(GenericBlock("cos", block_operator="cos"))
        # self.addConnection("time", "cos", input_port_name="IN1", output_port_name="OUT1")
        # self.addConnection("cos", "integration", input_port_name="IN", output_port_name="OUT1")
        self.addConnection("ic", "integration", input_port_name="IC")
        self.addConnection("integration", "OUT", output_port_name="OUT")

if __name__ == "__main__":

    backwards = IntegrationTest()
    forwards = IntegrationTest(integration=ForwardsEuler("integration"))
    trapezoid = IntegrationTest(integration=Trapezoid("integration"))

    sim1 = Simulator(backwards)
    sim2 = Simulator(forwards)
    sim3 = Simulator(trapezoid)

    end_time = 100.0
    DELTA_T = 0.01
    analytical = 3.21249210409227

    sim1.setDeltaT(DELTA_T)
    sim1.run(end_time)

    sim2.setDeltaT(end_time)
    sim2.run(ITERATIONS)

    sim3.setDeltaT(DELTA_T)
    sim3.run(end_time)
    print("Backwards Euler: ", backwards.getSignalHistory('OUT')[-1])
    print("Forwards Euler: ", forwards.getSignalHistory('OUT')[-1])
    print("Trapezoid Rule: ", trapezoid.getSignalHistory('OUT')[-1])
    testing if trapezoid = mean(backwards, forwards)
    print((backwards.getSignalHistory('OUT')[-1][1] + forwards.getSignalHistory('OUT')[-1][1]) / 2)
    print(f"{abs((backwards.getSignalHistory('OUT')[-1][1] + forwards.getSignalHistory('OUT')[-1][1]) / 2 - trapezoid.getSignalHistory('OUT')[-1][1]):.20f}")
    print(f"{abs(analytical - backwards.getSignalHistory('OUT')[-1][1]):.20f}")
    print(f"{abs(analytical - forwards.getSignalHistory('OUT')[-1][1]):.20f}")
    print(f"{abs(analytical - trapezoid.getSignalHistory('OUT')[-1][1]):.20f}")
