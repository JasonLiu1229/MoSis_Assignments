from fmpy import simulate_fmu
from fmpy.fmucontainer import create_fmu_container, Connection, Configuration, Component, Variable
from fmpy.validation import validate_fmu
from fmpy.util import compile_platform_binary
from fmpy.model_description import DefaultExperiment

def gen_image(x_axis, y_axis, title, x_label, y_label, legend):
	import matplotlib.pyplot as plt
	plt.figure()
	plt.plot(x_axis, y_axis)
	plt.title(title)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.legend(legend)
	png_title = title.replace(" ", "_")
	plt.savefig("assets/" + png_title + ".png")

if __name__ == "__main__":

	configuration = Configuration(
		fmiVersion='2.0',
		defaultExperiment=DefaultExperiment(
			startTime='0',
			stopTime='20',
			tolerance='1e-7',
			stepSize='0.004'
		),
		parallelDoStep=False,
		variables = [
			Variable(
				type='Real',
				initial='calculated',
				variability='continuous',
				causality='output',
				name='x',
				mapping=[('plant', 'x_output')]
			),
			Variable(
				type='Real',
				initial='calculated',
				variability='continuous',
				causality='output',
				name='theta',
				mapping=[('plant', 'theta_output')]
			),
			Variable(
				type='Real',
				initial='calculated',
				variability='continuous',
				causality='output',
				name='u_pid',
				mapping=[('pid', 'PIDCLBlock.u(t)')]
			),
		],
		components=[
			Component(
				filename='Plant.fmu',
				name='plant'
			),
			Component(
				filename='Controller.fmu',
				name='pid'
			)
		],
		connections=[
			Connection('pid', 'PIDCLBlock.u(t)', 'plant', 'u_input'),
			Connection('plant', 'x_output', 'pid', 'PIDCLBlock.x(t)')
		]
	)

	create_fmu_container(configuration, "Container.fmu")
	problems = validate_fmu("Container.fmu")
	if problems:
		print("PROBLEMS ENCOUNTERED WITH COMBINED FMU:")
		print(problems)
		exit()

	result = simulate_fmu("Container.fmu",
						  #debug_logging=True,
						  #fmi_call_logger=print,
						  stop_time=20,
						  output_interval=0.004)

	import matplotlib.pyplot as plt
 
	time = [r[0] for r in result]
	x = [r[1] for r in result]
	theta = [r[2] for r in result]
	u_pid = [r[3] for r in result]
 
	gen_image(time, x, "Position vs Time", "Time (s)", "Position (m)", ["Position"])
	gen_image(time, theta, "Angle vs Time", "Time (s)", "Angle (rad)", ["Angle"])
	gen_image(time, u_pid, "Control Signal vs Time", "Time (s)", "Control Signal (N)", ["Control Signal"])
