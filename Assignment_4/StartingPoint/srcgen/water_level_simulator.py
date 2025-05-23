"""Implementation of statechart water_level_simulator.
Generated by itemis CREATE code generator.
"""

import queue
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib')))
from yakindu.rx import Observable

class WaterLevelSimulator:
	"""Implementation of the state machine WaterLevelSimulator.
	"""

	class State:
		""" State Enum
		"""
		(
			main_region_o,
			main_region_or1no_flow,
			main_region_or1low_flow,
			main_region_or1b_no_flow,
			main_region_or1b_high_flow,
			main_region_or2sensor_good,
			main_region_or2sensor_broken,
			main_region_or3d,
			null_state
		) = range(9)
	
	
	def __init__(self):
		""" Declares all necessary variables including list of states, histories etc. 
		"""
		
		self.open_flow = None
		self.open_flow_value = None
		self.close_flow = None
		self.close_flow_value = None
		self.toggle_sensor_broken = None
		self.real_water_level = None
		self.real_water_level_value = None
		self.real_water_level_observable = Observable()
		self.sensor_reading = None
		self.sensor_reading_value = None
		self.sensor_reading_observable = Observable()
		
		self.__internal_event_queue = queue.Queue()
		self.in_event_queue = queue.Queue()
		self.LOW = 0
		self.HIGH = 1
		self.LOW_LVL = 500
		self.HIGH_LVL = 1500
		self.FLOW_RATE = 50
		self.__water_level = None
		self.water_lvl_changed = None
		
		# enumeration of all states:
		self.__State = WaterLevelSimulator.State
		self.__state_conf_vector_changed = None
		self.__state_vector = [None] * 4
		for __state_index in range(4):
			self.__state_vector[__state_index] = self.State.null_state
		
		# for timed statechart:
		self.timer_service = None
		self.__time_events = [None] * 2
		
		# initializations:
		#Default init sequence for statechart WaterLevelSimulator
		self.__water_level = self.LOW_LVL
		self.__is_executing = False
		self.__state_conf_vector_position = None
	
	def is_active(self):
		"""Checks if the state machine is active.
		"""
		return self.__state_vector[0] is not self.__State.null_state or self.__state_vector[1] is not self.__State.null_state or self.__state_vector[2] is not self.__State.null_state or self.__state_vector[3] is not self.__State.null_state
	
	def is_final(self):
		"""Checks if the statemachine is final.
		Always returns 'false' since this state machine can never become final.
		"""
		return False
			
	def is_state_active(self, state):
		"""Checks if the state is currently active.
		"""
		s = state
		if s == self.__State.main_region_o:
			return (self.__state_vector[0] >= self.__State.main_region_o)\
				and (self.__state_vector[0] <= self.__State.main_region_or3d)
		if s == self.__State.main_region_or1no_flow:
			return self.__state_vector[0] == self.__State.main_region_or1no_flow
		if s == self.__State.main_region_or1low_flow:
			return self.__state_vector[0] == self.__State.main_region_or1low_flow
		if s == self.__State.main_region_or1b_no_flow:
			return self.__state_vector[1] == self.__State.main_region_or1b_no_flow
		if s == self.__State.main_region_or1b_high_flow:
			return self.__state_vector[1] == self.__State.main_region_or1b_high_flow
		if s == self.__State.main_region_or2sensor_good:
			return self.__state_vector[2] == self.__State.main_region_or2sensor_good
		if s == self.__State.main_region_or2sensor_broken:
			return self.__state_vector[2] == self.__State.main_region_or2sensor_broken
		if s == self.__State.main_region_or3d:
			return self.__state_vector[3] == self.__State.main_region_or3d
		return False
		
	def time_elapsed(self, event_id):
		"""Add time events to in event queue
		"""
		if event_id in range(2):
			self.in_event_queue.put(lambda: self.raise_time_event(event_id))
			self.run_cycle()
	
	def raise_time_event(self, event_id):
		"""Raise timed events using the event_id.
		"""
		self.__time_events[event_id] = True
	
	def __execute_queued_event(self, func):
		func()
	
	def __get_next_event(self):
		if not self.__internal_event_queue.empty():
			return self.__internal_event_queue.get()
		if not self.in_event_queue.empty():
			return self.in_event_queue.get()
		return None
	
	
	def raise_water_lvl_changed(self):
		"""Raise method for event water_lvl_changed.
		"""
		self.__internal_event_queue.put(self.__raise_water_lvl_changed_call)
	
	def __raise_water_lvl_changed_call(self):
		"""Raise callback for event water_lvl_changed.
		"""
		self.water_lvl_changed = True
	
	def raise_open_flow(self, value):
		"""Raise method for event open_flow.
		"""
		self.in_event_queue.put(lambda: self.__raise_open_flow_call(value))
		self.run_cycle()
	
	def __raise_open_flow_call(self, value):
		"""Raise callback for event open_flow.
		"""
		self.open_flow = True
		self.open_flow_value = value
	
	def raise_close_flow(self, value):
		"""Raise method for event close_flow.
		"""
		self.in_event_queue.put(lambda: self.__raise_close_flow_call(value))
		self.run_cycle()
	
	def __raise_close_flow_call(self, value):
		"""Raise callback for event close_flow.
		"""
		self.close_flow = True
		self.close_flow_value = value
	
	def raise_toggle_sensor_broken(self):
		"""Raise method for event toggle_sensor_broken.
		"""
		self.in_event_queue.put(self.__raise_toggle_sensor_broken_call)
		self.run_cycle()
	
	def __raise_toggle_sensor_broken_call(self):
		"""Raise callback for event toggle_sensor_broken.
		"""
		self.toggle_sensor_broken = True
	
	def __entry_action_main_region_o_r1_low_flow(self):
		"""Entry action for state 'LowFlow'..
		"""
		#Entry action for state 'LowFlow'.
		self.timer_service.set_timer(self, 0, 100, False)
		
	def __entry_action_main_region_o_r1b_high_flow(self):
		"""Entry action for state 'HighFlow'..
		"""
		#Entry action for state 'HighFlow'.
		self.timer_service.set_timer(self, 1, 100, False)
		
	def __entry_action_main_region_o_r3_d(self):
		"""Entry action for state 'D'..
		"""
		#Entry action for state 'D'.
		self.real_water_level_observable.next(self.__water_level)
		self.sensor_reading_observable.next(99000 if (self.__state_vector[2] == self.State.main_region_or2sensor_broken) else self.__water_level)
		
	def __exit_action_main_region_o_r1_low_flow(self):
		"""Exit action for state 'LowFlow'..
		"""
		#Exit action for state 'LowFlow'.
		self.timer_service.unset_timer(self, 0)
		
	def __exit_action_main_region_o_r1b_high_flow(self):
		"""Exit action for state 'HighFlow'..
		"""
		#Exit action for state 'HighFlow'.
		self.timer_service.unset_timer(self, 1)
		
	def __enter_sequence_main_region_o_default(self):
		"""'default' enter sequence for state O.
		"""
		#'default' enter sequence for state O
		self.__enter_sequence_main_region_o_r1_default()
		self.__enter_sequence_main_region_o_r1b_default()
		self.__enter_sequence_main_region_o_r2_default()
		self.__enter_sequence_main_region_o_r3_default()
		
	def __enter_sequence_main_region_o_r1_no_flow_default(self):
		"""'default' enter sequence for state NoFlow.
		"""
		#'default' enter sequence for state NoFlow
		self.__state_vector[0] = self.State.main_region_or1no_flow
		self.__state_conf_vector_position = 0
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_o_r1_low_flow_default(self):
		"""'default' enter sequence for state LowFlow.
		"""
		#'default' enter sequence for state LowFlow
		self.__entry_action_main_region_o_r1_low_flow()
		self.__state_vector[0] = self.State.main_region_or1low_flow
		self.__state_conf_vector_position = 0
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_o_r1b_no_flow_default(self):
		"""'default' enter sequence for state NoFlow.
		"""
		#'default' enter sequence for state NoFlow
		self.__state_vector[1] = self.State.main_region_or1b_no_flow
		self.__state_conf_vector_position = 1
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_o_r1b_high_flow_default(self):
		"""'default' enter sequence for state HighFlow.
		"""
		#'default' enter sequence for state HighFlow
		self.__entry_action_main_region_o_r1b_high_flow()
		self.__state_vector[1] = self.State.main_region_or1b_high_flow
		self.__state_conf_vector_position = 1
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_o_r2_sensor_good_default(self):
		"""'default' enter sequence for state SensorGood.
		"""
		#'default' enter sequence for state SensorGood
		self.__state_vector[2] = self.State.main_region_or2sensor_good
		self.__state_conf_vector_position = 2
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_o_r2_sensor_broken_default(self):
		"""'default' enter sequence for state SensorBroken.
		"""
		#'default' enter sequence for state SensorBroken
		self.__state_vector[2] = self.State.main_region_or2sensor_broken
		self.__state_conf_vector_position = 2
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_o_r3_d_default(self):
		"""'default' enter sequence for state D.
		"""
		#'default' enter sequence for state D
		self.__entry_action_main_region_o_r3_d()
		self.__state_vector[3] = self.State.main_region_or3d
		self.__state_conf_vector_position = 3
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_default(self):
		"""'default' enter sequence for region main region.
		"""
		#'default' enter sequence for region main region
		self.__react_main_region__entry_default()
		
	def __enter_sequence_main_region_o_r1_default(self):
		"""'default' enter sequence for region r1.
		"""
		#'default' enter sequence for region r1
		self.__react_main_region_o_r1__entry_default()
		
	def __enter_sequence_main_region_o_r1b_default(self):
		"""'default' enter sequence for region r1b.
		"""
		#'default' enter sequence for region r1b
		self.__react_main_region_o_r1b__entry_default()
		
	def __enter_sequence_main_region_o_r2_default(self):
		"""'default' enter sequence for region r2.
		"""
		#'default' enter sequence for region r2
		self.__react_main_region_o_r2__entry_default()
		
	def __enter_sequence_main_region_o_r3_default(self):
		"""'default' enter sequence for region r3.
		"""
		#'default' enter sequence for region r3
		self.__react_main_region_o_r3__entry_default()
		
	def __exit_sequence_main_region_o_r1_no_flow(self):
		"""Default exit sequence for state NoFlow.
		"""
		#Default exit sequence for state NoFlow
		self.__state_vector[0] = self.State.main_region_o
		self.__state_conf_vector_position = 0
		
	def __exit_sequence_main_region_o_r1_low_flow(self):
		"""Default exit sequence for state LowFlow.
		"""
		#Default exit sequence for state LowFlow
		self.__state_vector[0] = self.State.main_region_o
		self.__state_conf_vector_position = 0
		self.__exit_action_main_region_o_r1_low_flow()
		
	def __exit_sequence_main_region_o_r1b_no_flow(self):
		"""Default exit sequence for state NoFlow.
		"""
		#Default exit sequence for state NoFlow
		self.__state_vector[1] = self.State.main_region_o
		self.__state_conf_vector_position = 1
		
	def __exit_sequence_main_region_o_r1b_high_flow(self):
		"""Default exit sequence for state HighFlow.
		"""
		#Default exit sequence for state HighFlow
		self.__state_vector[1] = self.State.main_region_o
		self.__state_conf_vector_position = 1
		self.__exit_action_main_region_o_r1b_high_flow()
		
	def __exit_sequence_main_region_o_r2_sensor_good(self):
		"""Default exit sequence for state SensorGood.
		"""
		#Default exit sequence for state SensorGood
		self.__state_vector[2] = self.State.main_region_o
		self.__state_conf_vector_position = 2
		
	def __exit_sequence_main_region_o_r2_sensor_broken(self):
		"""Default exit sequence for state SensorBroken.
		"""
		#Default exit sequence for state SensorBroken
		self.__state_vector[2] = self.State.main_region_o
		self.__state_conf_vector_position = 2
		
	def __exit_sequence_main_region_o_r3_d(self):
		"""Default exit sequence for state D.
		"""
		#Default exit sequence for state D
		self.__state_vector[3] = self.State.main_region_o
		self.__state_conf_vector_position = 3
		
	def __exit_sequence_main_region(self):
		"""Default exit sequence for region main region.
		"""
		#Default exit sequence for region main region
		state = self.__state_vector[0]
		if state == self.State.main_region_or1no_flow:
			self.__exit_sequence_main_region_o_r1_no_flow()
		elif state == self.State.main_region_or1low_flow:
			self.__exit_sequence_main_region_o_r1_low_flow()
		state = self.__state_vector[1]
		if state == self.State.main_region_or1b_no_flow:
			self.__exit_sequence_main_region_o_r1b_no_flow()
		elif state == self.State.main_region_or1b_high_flow:
			self.__exit_sequence_main_region_o_r1b_high_flow()
		state = self.__state_vector[2]
		if state == self.State.main_region_or2sensor_good:
			self.__exit_sequence_main_region_o_r2_sensor_good()
		elif state == self.State.main_region_or2sensor_broken:
			self.__exit_sequence_main_region_o_r2_sensor_broken()
		state = self.__state_vector[3]
		if state == self.State.main_region_or3d:
			self.__exit_sequence_main_region_o_r3_d()
		
	def __react_main_region_o_r1__entry_default(self):
		"""Default react sequence for initial entry .
		"""
		#Default react sequence for initial entry 
		self.__enter_sequence_main_region_o_r1_no_flow_default()
		
	def __react_main_region_o_r1b__entry_default(self):
		"""Default react sequence for initial entry .
		"""
		#Default react sequence for initial entry 
		self.__enter_sequence_main_region_o_r1b_no_flow_default()
		
	def __react_main_region_o_r2__entry_default(self):
		"""Default react sequence for initial entry .
		"""
		#Default react sequence for initial entry 
		self.__enter_sequence_main_region_o_r2_sensor_good_default()
		
	def __react_main_region_o_r3__entry_default(self):
		"""Default react sequence for initial entry .
		"""
		#Default react sequence for initial entry 
		self.__enter_sequence_main_region_o_r3_d_default()
		
	def __react_main_region__entry_default(self):
		"""Default react sequence for initial entry .
		"""
		#Default react sequence for initial entry 
		self.__enter_sequence_main_region_o_default()
		
	def __react(self, transitioned_before):
		"""Implementation of __react function.
		"""
		#State machine reactions.
		return transitioned_before
	
	
	def __main_region_o_react(self, transitioned_before):
		"""Implementation of __main_region_o_react function.
		"""
		#The reactions of state O.
		return self.__react(transitioned_before)
	
	
	def __main_region_o_r1_no_flow_react(self, transitioned_before):
		"""Implementation of __main_region_o_r1_no_flow_react function.
		"""
		#The reactions of state NoFlow.
		transitioned_after = self.__main_region_o_react(transitioned_before)
		if transitioned_after < 0:
			if (self.open_flow) and (self.open_flow_value == self.LOW):
				self.__exit_sequence_main_region_o_r1_no_flow()
				self.__enter_sequence_main_region_o_r1_low_flow_default()
				transitioned_after = 0
		return transitioned_after
	
	
	def __main_region_o_r1_low_flow_react(self, transitioned_before):
		"""Implementation of __main_region_o_r1_low_flow_react function.
		"""
		#The reactions of state LowFlow.
		transitioned_after = self.__main_region_o_react(transitioned_before)
		if transitioned_after < 0:
			if (self.close_flow) and (self.close_flow_value == self.LOW):
				self.__exit_sequence_main_region_o_r1_low_flow()
				self.__enter_sequence_main_region_o_r1_no_flow_default()
				transitioned_after = 0
			elif (self.__time_events[0]) and (self.__water_level > self.LOW_LVL):
				self.__exit_sequence_main_region_o_r1_low_flow()
				self.__water_level = (((((self.__water_level * 5) + self.LOW_LVL)) / 6) - 1)
				self.raise_water_lvl_changed()
				self.__time_events[0] = False
				self.__enter_sequence_main_region_o_r1_low_flow_default()
				transitioned_after = 0
		return transitioned_after
	
	
	def __main_region_o_r1b_no_flow_react(self, transitioned_before):
		"""Implementation of __main_region_o_r1b_no_flow_react function.
		"""
		#The reactions of state NoFlow.
		transitioned_after = transitioned_before
		if transitioned_after < 1:
			if (self.open_flow) and (self.open_flow_value == self.HIGH):
				self.__exit_sequence_main_region_o_r1b_no_flow()
				self.__enter_sequence_main_region_o_r1b_high_flow_default()
				transitioned_after = 1
		return transitioned_after
	
	
	def __main_region_o_r1b_high_flow_react(self, transitioned_before):
		"""Implementation of __main_region_o_r1b_high_flow_react function.
		"""
		#The reactions of state HighFlow.
		transitioned_after = transitioned_before
		if transitioned_after < 1:
			if (self.close_flow) and (self.close_flow_value == self.HIGH):
				self.__exit_sequence_main_region_o_r1b_high_flow()
				self.__enter_sequence_main_region_o_r1b_no_flow_default()
				transitioned_after = 1
			elif (self.__time_events[1]) and (self.__water_level < self.HIGH_LVL):
				self.__exit_sequence_main_region_o_r1b_high_flow()
				self.__water_level = (((((self.__water_level * 5) + self.HIGH_LVL)) / 6) + 1)
				self.raise_water_lvl_changed()
				self.__time_events[1] = False
				self.__enter_sequence_main_region_o_r1b_high_flow_default()
				transitioned_after = 1
		return transitioned_after
	
	
	def __main_region_o_r2_sensor_good_react(self, transitioned_before):
		"""Implementation of __main_region_o_r2_sensor_good_react function.
		"""
		#The reactions of state SensorGood.
		transitioned_after = transitioned_before
		if transitioned_after < 2:
			if self.toggle_sensor_broken:
				self.__exit_sequence_main_region_o_r2_sensor_good()
				self.raise_water_lvl_changed()
				self.__enter_sequence_main_region_o_r2_sensor_broken_default()
				transitioned_after = 2
		return transitioned_after
	
	
	def __main_region_o_r2_sensor_broken_react(self, transitioned_before):
		"""Implementation of __main_region_o_r2_sensor_broken_react function.
		"""
		#The reactions of state SensorBroken.
		transitioned_after = transitioned_before
		if transitioned_after < 2:
			if self.toggle_sensor_broken:
				self.__exit_sequence_main_region_o_r2_sensor_broken()
				self.raise_water_lvl_changed()
				self.__enter_sequence_main_region_o_r2_sensor_good_default()
				transitioned_after = 2
		return transitioned_after
	
	
	def __main_region_o_r3_d_react(self, transitioned_before):
		"""Implementation of __main_region_o_r3_d_react function.
		"""
		#The reactions of state D.
		transitioned_after = transitioned_before
		if transitioned_after < 3:
			if self.water_lvl_changed:
				self.__exit_sequence_main_region_o_r3_d()
				self.__enter_sequence_main_region_o_r3_d_default()
				transitioned_after = 3
		return transitioned_after
	
	
	def __clear_in_events(self):
		"""Implementation of __clear_in_events function.
		"""
		self.open_flow = False
		self.close_flow = False
		self.toggle_sensor_broken = False
		self.__time_events[0] = False
		self.__time_events[1] = False
	
	
	def __clear_internal_events(self):
		"""Implementation of __clear_internal_events function.
		"""
		self.water_lvl_changed = False
	
	
	def __micro_step(self):
		"""Implementation of __micro_step function.
		"""
		transitioned = -1
		self.__state_conf_vector_position = 0
		state = self.__state_vector[0]
		if state == self.State.main_region_or1no_flow:
			transitioned = self.__main_region_o_r1_no_flow_react(transitioned)
		elif state == self.State.main_region_or1low_flow:
			transitioned = self.__main_region_o_r1_low_flow_react(transitioned)
		if self.__state_conf_vector_position < 1:
			state = self.__state_vector[1]
			if state == self.State.main_region_or1b_no_flow:
				transitioned = self.__main_region_o_r1b_no_flow_react(transitioned)
			elif state == self.State.main_region_or1b_high_flow:
				transitioned = self.__main_region_o_r1b_high_flow_react(transitioned)
		if self.__state_conf_vector_position < 2:
			state = self.__state_vector[2]
			if state == self.State.main_region_or2sensor_good:
				transitioned = self.__main_region_o_r2_sensor_good_react(transitioned)
			elif state == self.State.main_region_or2sensor_broken:
				transitioned = self.__main_region_o_r2_sensor_broken_react(transitioned)
		if self.__state_conf_vector_position < 3:
			state = self.__state_vector[3]
			if state == self.State.main_region_or3d:
				self.__main_region_o_r3_d_react(transitioned)
	
	
	def run_cycle(self):
		"""Implementation of run_cycle function.
		"""
		#Performs a 'run to completion' step.
		if self.timer_service is None:
			raise ValueError('Timer service must be set.')
		
		if self.__is_executing:
			return
		self.__is_executing = True
		next_event = self.__get_next_event()
		if next_event is not None:
			self.__execute_queued_event(next_event)
		condition_0 = True
		while condition_0:
			self.__micro_step()
			self.__clear_in_events()
			self.__clear_internal_events()
			condition_0 = False
			next_event = self.__get_next_event()
			if next_event is not None:
				self.__execute_queued_event(next_event)
				condition_0 = True
		self.__is_executing = False
	
	
	def enter(self):
		"""Implementation of enter function.
		"""
		#Activates the state machine.
		if self.timer_service is None:
			raise ValueError('Timer service must be set.')
		
		if self.__is_executing:
			return
		self.__is_executing = True
		#Default enter sequence for statechart WaterLevelSimulator
		self.__enter_sequence_main_region_default()
		self.__is_executing = False
	
	
	def exit(self):
		"""Implementation of exit function.
		"""
		#Deactivates the state machine.
		if self.__is_executing:
			return
		self.__is_executing = True
		#Default exit sequence for statechart WaterLevelSimulator
		self.__exit_sequence_main_region()
		self.__state_vector[0] = self.State.null_state
		self.__state_vector[1] = self.State.null_state
		self.__state_vector[2] = self.State.null_state
		self.__state_vector[3] = self.State.null_state
		self.__state_conf_vector_position = 3
		self.__is_executing = False
	
	
	def trigger_without_event(self):
		"""Implementation of triggerWithoutEvent function.
		"""
		self.run_cycle()
	
