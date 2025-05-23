import functools
import dataclasses
from lib.test import run_scenarios, AbstractEnvironmentState

from srcgen.lock_controller import LockController
# from srcgen.solution import Solution as LockController # Teacher's solution

# For each test scenario, sends a sequence of timed input events to the statechart, and checks if the expected sequence of timed output events occurs.

# Each timed event is a tuple (timestamp, event_name, parameter_value)
# For events that don't have a parameter, the parameter value is always 'None'.
# Timestamps are in nanoseconds since simulation start!

SCENARIOS = [
{
    "name": "normal operation, serve two requests",
    "input_events": [
        (0, "water_lvl", 508),
        (2393556604, "request_lvl_change", None),
        (4493556604, "water_lvl", 675),
        (4593556604, "water_lvl", 811),
        (4693556604, "water_lvl", 926),
        (4793556604, "water_lvl", 1025),
        (4893556604, "water_lvl", 1105),
        (4993556604, "water_lvl", 1176),
        (5093556604, "water_lvl", 1228),
        (5193556604, "water_lvl", 1276),
        (5293556604, "water_lvl", 1316),
        (5393556604, "water_lvl", 1352),
        (5493556604, "water_lvl", 1375),
        (5593556604, "water_lvl", 1395),
        (5693556604, "water_lvl", 1419),
        (5793556604, "water_lvl", 1433),
        (5893556604, "water_lvl", 1443),
        (5993556604, "water_lvl", 1460),
        (6093556604, "water_lvl", 1470),
        (6193556604, "water_lvl", 1476),
        (6293556604, "water_lvl", 1483),
        (6393556604, "water_lvl", 1482),
        (6493556604, "water_lvl", 1491),
        (6593556604, "water_lvl", 1496),
        (6693556604, "water_lvl", 1497),
        (6793556604, "water_lvl", 1498),
        (6893556604, "water_lvl", 1496),
        (6993556604, "water_lvl", 1501),
        (7093556604, "water_lvl", 1504),
        (7193556604, "water_lvl", 1509),
        (9193747734, "request_lvl_change", None),
        (11293747734, "water_lvl", 1341),
        (11393747734, "water_lvl", 1197),
        (11493747734, "water_lvl", 1084),
        (11593747734, "water_lvl", 981),
        (11693747734, "water_lvl", 906),
        (11793747734, "water_lvl", 836),
        (11893747734, "water_lvl", 774),
        (11993747734, "water_lvl", 735),
        (12093747734, "water_lvl", 692),
        (12193747734, "water_lvl", 664),
        (12293747734, "water_lvl", 636),
        (12393747734, "water_lvl", 606),
        (12493747734, "water_lvl", 592),
        (12593747734, "water_lvl", 581),
        (12693747734, "water_lvl", 561),
        (12793747734, "water_lvl", 551),
        (12893747734, "water_lvl", 548),
        (12993747734, "water_lvl", 533),
        (13093747734, "water_lvl", 531),
        (13193747734, "water_lvl", 522),
        (13293747734, "water_lvl", 525),
        (13393747734, "water_lvl", 520),
        (13493747734, "water_lvl", 513),
        (13593747734, "water_lvl", 507),
        (13693747734, "water_lvl", 507),
        (13793747734, "water_lvl", 507),
        (13893747734, "water_lvl", 510),
        (13993747734, "water_lvl", 501),
        (14093747734, "water_lvl", 504),
    ],
    "output_events": [
        (0, "open_doors", 0),
        (0, "green_light", 0),
        (2393556604, "red_light", 0),
        (2393556604, "set_request_pending", True),
        (4393556604, "close_doors", 0),
        (4393556604, "open_flow", 1),
        (7193556604, "close_flow", 1),
        (7193556604, "set_request_pending", False),
        (7193556604, "open_doors", 1),
        (7193556604, "green_light", 1),
        (9193747734, "red_light", 1),
        (9193747734, "set_request_pending", True),
        (11193747734, "close_doors", 1),
        (11193747734, "open_flow", 0),
        (14193747734, "close_flow", 0),
        (14193747734, "set_request_pending", False),
        (14193747734, "open_doors", 0),
        (14193747734, "green_light", 0),
    ],
},
{
    "name": "break sensor, fix sensor, then change water lvl",
    "input_events": [
        (0, "water_lvl", 508),
        (2084169493, "water_lvl", 99007),
        (4084274216, "water_lvl", 504),
        (5420871976, "resume", None),
        (7100735485, "request_lvl_change", None),
        (9200735485, "water_lvl", 670),
        (9300735485, "water_lvl", 812),
        (9400735485, "water_lvl", 927),
        (9500735485, "water_lvl", 1028),
        (9600735485, "water_lvl", 1104),
        (9700735485, "water_lvl", 1173),
        (9800735485, "water_lvl", 1231),
        (9900735485, "water_lvl", 1281),
        (10000735485, "water_lvl", 1316),
        (10100735485, "water_lvl", 1346),
        (10200735485, "water_lvl", 1378),
        (10300735485, "water_lvl", 1399),
        (10400735485, "water_lvl", 1414),
        (10500735485, "water_lvl", 1436),
        (10600735485, "water_lvl", 1450),
        (10700735485, "water_lvl", 1459),
        (10800735485, "water_lvl", 1469),
        (10900735485, "water_lvl", 1471),
        (11000735485, "water_lvl", 1481),
        (11100735485, "water_lvl", 1488),
        (11200735485, "water_lvl", 1490),
        (11300735485, "water_lvl", 1492),
        (11400735485, "water_lvl", 1491),
        (11500735485, "water_lvl", 1497),
        (11600735485, "water_lvl", 1501),
        (11700735485, "water_lvl", 1506),
        (11800735485, "water_lvl", 1508),
        (11900735485, "water_lvl", 1504),
    ],
    "output_events": [
        (0, "open_doors", 0),
        (0, "green_light", 0),
        (2084169493, "red_light", 0),
        (2084169493, "close_doors", 0),
        (2084169493, "set_sensor_broken", None),
        (5420871976, "open_doors", 0),
        (5420871976, "green_light", 0),
        (7100735485, "red_light", 0),
        (7100735485, "set_request_pending", True),
        (9100735485, "close_doors", 0),
        (9100735485, "open_flow", 1),
        (11900735485, "close_flow", 1),
        (11900735485, "set_request_pending", False),
        (11900735485, "open_doors", 1),
        (11900735485, "green_light", 1),
    ],
},
{
    "name": "break sensor DURING water lvl change, then fix and resume",
    "input_events": [
        (0, "water_lvl", 508),
        (2661508910, "request_lvl_change", None),
        (4761508910, "water_lvl", 675),
        (4861508910, "water_lvl", 811),
        (4961508910, "water_lvl", 926),
        (5061508910, "water_lvl", 1025),
        (5093300938, "water_lvl", 99004),
        (7821829184, "water_lvl", 1028),
        (9213791769, "resume", None),
        (9313791769, "water_lvl", 1104),
        (9413791769, "water_lvl", 1173),
        (9513791769, "water_lvl", 1231),
        (9613791769, "water_lvl", 1281),
        (9713791769, "water_lvl", 1316),
        (9813791769, "water_lvl", 1346),
        (9913791769, "water_lvl", 1378),
        (10013791769, "water_lvl", 1399),
        (10113791769, "water_lvl", 1414),
        (10213791769, "water_lvl", 1436),
        (10313791769, "water_lvl", 1450),
        (10413791769, "water_lvl", 1459),
        (10513791769, "water_lvl", 1469),
        (10613791769, "water_lvl", 1471),
        (10713791769, "water_lvl", 1481),
        (10813791769, "water_lvl", 1488),
        (10913791769, "water_lvl", 1490),
        (11013791769, "water_lvl", 1492),
        (11113791769, "water_lvl", 1491),
        (11213791769, "water_lvl", 1497),
        (11313791769, "water_lvl", 1501),
        (11413791769, "water_lvl", 1506),
        (11513791769, "water_lvl", 1508),
        (11613791769, "water_lvl", 1504),
    ],
    "output_events": [
        (0, "open_doors", 0),
        (0, "green_light", 0),
        (2661508910, "red_light", 0),
        (2661508910, "set_request_pending", True),
        (4661508910, "close_doors", 0),
        (4661508910, "open_flow", 1),
        (5093300938, "close_flow", 1),
        (5093300938, "set_sensor_broken", None),
        (9213791769, "open_flow", 1),
        (11613791769, "close_flow", 1),
        (11613791769, "set_request_pending", False),
        (11613791769, "open_doors", 1),
        (11613791769, "green_light", 1),
    ],
},
{
    # Test obstruct door
    "name": "obstruct door and break sensor while obstructing",
    "input_events": [
        (0, "water_lvl", 500),
        (1000000000, "request_lvl_change", None),
        (2500000000, "door_obstructed", None),
        (4000000000, "water_lvl", 10000),
        (4500000000, "water_lvl", 1000),
        (5000000000, "resume", None),
        (6000000000, "water_lvl", 1500)
    ],
    "output_events": [
        (0, "open_doors", 0),
        (0, "green_light", 0),
        (1000000000, "red_light", 0),
        (1000000000, "set_request_pending", True),
        (4000000000, "close_doors", 0), # close doors not after 2s, but because it enters emergency mode
        (4000000000, "set_sensor_broken", None),
        (5000000000, "open_flow", 1), # open correct flow, door stays closed
        (7000000000, "close_flow", 1),
        (7000000000, "set_request_pending", False),
        (7000000000, "open_doors", 1),
        (7000000000, "green_light", 1),
    ]
},
{
    # Test if it can accept requests when in emergency mode and proceed with the request when it resumes.
    "name": "Break sensor, request water change, then resume",
    "input_events": [
        (0, "water_lvl", 500),
        (500000000, "water_lvl", 10000),
        (1000000000, "request_lvl_change", None),
        (1500000000, "water_lvl", 1000),
        (2000000000, "resume", None),
        (3000000000, "water_lvl", 1500)
    ],
    "output_events": [
        (0, "open_doors", 0),
        (0, "green_light", 0),
        (500000000, "red_light", 0),
        (500000000, "close_doors", 0),
        (500000000, "set_sensor_broken", None),
        (1000000000, "set_request_pending", True), # accept request
        (2000000000, "open_flow", 1), # immediately open the correct flow, doors stay closed
        (4000000000, "close_flow", 1),
        (4000000000, "set_request_pending", False),
        (4000000000, "open_doors", 1),
        (4000000000, "green_light", 1),
    ]
}
]

LOW = 0
HIGH = 1

# Simulated state of the 'plant'.
# This is used for checking whether an event has any effect wrt. idempotency
@dataclasses.dataclass
class PlantState(AbstractEnvironmentState):
    # initial state of the plant
    door_low_open: bool = False
    door_high_open: bool = False
    flow_low_open: bool = False
    flow_high_open: bool = False
    light_low: str = "RED"
    light_high: str = "RED"
    request_is_pending: bool = False
    sensor_is_broken: bool = False

    def handle_event(self, event_name, param):
        if event_name == "open_doors":
            if param == LOW:
                return dataclasses.replace(self, door_low_open=True)
            elif param == HIGH:
                return dataclasses.replace(self, door_high_open=True)
            else:
                raise Exception(f"invalid param for event '{event_name}': {param}")
        elif event_name == "close_doors":
            if param == LOW:
                return dataclasses.replace(self, door_low_open=False)
            elif param == HIGH:
                return dataclasses.replace(self, door_high_open=False)
            else:
                raise Exception(f"invalid param for event '{event_name}': {param}")
        elif event_name == "open_flow":
            if param == LOW:
                return dataclasses.replace(self, flow_low_open=True)
            elif param == HIGH:
                return dataclasses.replace(self, flow_high_open=True)
            else:
                raise Exception(f"invalid param for event '{event_name}': {param}")
        elif event_name == "close_flow":
            if param == LOW:
                return dataclasses.replace(self, flow_low_open=False)
            elif param == HIGH:
                return dataclasses.replace(self, flow_high_open=False)
            else:
                raise Exception(f"invalid param for event '{event_name}': {param}")
        elif event_name == "green_light":
            if param == LOW:
                return dataclasses.replace(self, light_low="GREEN")
            elif param == HIGH:
                return dataclasses.replace(self, light_high="GREEN")
            else:
                raise Exception(f"invalid param for event '{event_name}': {param}")
        elif event_name == "red_light":
            if param == LOW:
                return dataclasses.replace(self, light_low="RED")
            elif param == HIGH:
                return dataclasses.replace(self, light_high="RED")
            else:
                raise Exception(f"invalid param for event '{event_name}': {param}")
        elif event_name == "set_request_pending":
            return dataclasses.replace(self, request_is_pending=param)
        elif event_name == "set_sensor_broken":
            return dataclasses.replace(self, sensor_is_broken=param)
        else:
            raise Exception("don't know how to handle event:", event_name)

if __name__ == "__main__":
    run_scenarios(SCENARIOS, LockController, PlantState, verbose=False)
