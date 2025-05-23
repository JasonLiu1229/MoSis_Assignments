from simulate import singleSimExpOne, singleSimExpTwo, simPIDControlModel

import os
import pandas as pd
import matplotlib.pyplot as plt
import queue
import concurrent.futures
import numpy as np

def sumSquaredError(trace_file: str, calibration_file: str):
    """Calculate the sum of squared errors between the model output and calibration data.
    
    Args:
        trace_file (str): The trace file.
        calibration_file (str): The calibration file.
        
    Returns:
        float: The sum of squared errors.
    """
    trace_data = None
    calibration_data = None
    with open(trace_file, "r", encoding="utf-8") as f:
        trace_data = f.readlines()[1:]
    with open(calibration_file, "r", encoding="utf-8") as f:
        calibration_data = f.readlines()[1:]
    
    for i, data in enumerate(trace_data):
        trace_data[i] = float(data.split(",")[1])
    for i, data in enumerate(calibration_data):
        calibration_data[i] = float(data.split(",")[1])

    error = 0
    for trace, calibration in zip(trace_data, calibration_data):
        error += (trace - calibration)**2
    
    return error

def smallestError(trace_dir:str, calibration_file:str):
    """Find the smallest error between the model output and calibration data.
    
    Args:
        trace_dir (str): The directory containing the trace files.
        calibration_file (str): The calibration file.
        
    Returns:
        tuple: The smallest error and the file with the smallest error.
    """
    print("Finding smallest error")
    smallest_error = None
    smallest_error_file = None
    for file in os.listdir(trace_dir):
        error = sumSquaredError(os.path.join(trace_dir, file), calibration_file)
        if smallest_error is None or error < smallest_error:
            print(f"Current smallest error: {error}")
            print(f"File: {file}")
            smallest_error = error
            smallest_error_file = file
    
    return (smallest_error, smallest_error_file)


def smallestErrorMultiThread(q: queue.Queue, calibration_file):
    """Find the smallest error between the model output and calibration data.
    
    Args:
        q (queue.Queue): multithreaded queue to receive data from simulations.\
        Received value should be of (param_value, data) and last value should be None.
        calibration_file (str): The calibration file.
        
    Returns:
        tuple: The smallest error and the data with the smallest error.
    """

    print("Calculating errors in different thread", flush=True)
    smallest_error = None
    smallest_error_data = None
    param_value = None

    calibration_data = None

    with open(calibration_file, "r", encoding="utf-8") as f:
        calibration_data = f.readlines()[1:]

    for i, data in enumerate(calibration_data):
        calibration_data[i] = float(data.split(",")[1])
    
    while (trace_data := q.get()) is not None:
        error = 0
        for trace, calibration in zip(trace_data[1], calibration_data):
            error += (trace - calibration)**2
        if smallest_error is None or error < smallest_error:
            smallest_error = error
            smallest_error_data = trace_data[1]
            param_value = trace_data[0]
            print(f"Current smallest error: {smallest_error} for value {param_value}")
    print(f"Smallest error: {smallest_error} for value {param_value}")
    return (smallest_error, smallest_error_data, param_value)


def plotData(param_value, error_value, calibration_file, output_file, param_name):
    """Plot the model data and the calibration data
    
    Args:
        param_value (str): Value of parameter, part of file name to read.
        error_value (str): Value of smallest error, part of file name.
        calibration_file (str): File name to open for calibration data.
        output_file (str): Part of output file name.
        param_name (str): Label on y value.
    """
    data1 = pd.read_csv(f"answers/part_2/{output_file}_{param_value}_{error_value}.csv")
    data2 = pd.read_csv(calibration_file)
    
    extracted_data1 = data1.iloc[:, 1]
    extracted_data2 = data2.iloc[:, 1]
    
    plt.plot(extracted_data2, label="Calibration Data", color="blue")
    plt.plot(extracted_data1, label="Model Output", color="red")
    
    plt.xlabel("Iteration")
    plt.ylabel(param_name)
    plt.title("Model Output vs Calibration Data")
    
    plt.legend()
    plt.grid(True)
    
    plt.savefig(f"assets/part_2/{output_file}_comb.png")
    
    plt.figure()
    plt.plot(extracted_data1, label="Model Output", color="red")
    plt.xlabel("Iteration")
    plt.ylabel(param_name)
    plt.title("Model Output")
    
    plt.legend()
    plt.grid(True)
    
    plt.savefig(f"assets/part_2/{output_file}_rl.png")
    
    plt.figure()
    plt.plot(extracted_data2, label="Calibration Output", color="blue")
    plt.xlabel("Iteration")
    plt.ylabel(param_name)
    plt.title("Calibration Data")
    
    plt.legend()
    plt.grid(True)
    
    plt.savefig(f"assets/part_2/{output_file}_sim.png")


def runExperiment(exp=1, interval=5.00/10000):
    """Run experiment one. Copy the trace file with the smallest error to the answers folder.

    Args:
        exp (int): Experiment number to run. Either 1 or 2. Default to 1.
        interval (float, optional): The interval to increment d_c by. Defaults to 5.00/10000.
        
    Returns:
        None
    """
    # Ensure the 'traces' directory exists and create the 'exp1' subdirectory
    # os.makedirs('traces', exist_ok=True)
    # os.makedirs(f'traces/exp{exp}', exist_ok=True)

    if exp == 1: 
        calibration_file = "calibration_data_d_c.csv"
        output_file = "experiment_one_traces"
        simulate_function = singleSimExpOne
        param_name = "x"
    else:
        calibration_file = "calibration_data_d_p.csv"
        output_file = "experiment_two_traces"
        simulate_function = singleSimExpTwo
        param_name = "theta"

    # Create new thread to compare data
    error_output = None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        q = queue.Queue()

        future = executor.submit(smallestErrorMultiThread, q, calibration_file)
        
        i = 0.00
        k = 0
        while i < 5.00:
            print("Running simulation ", k)
            k += 1
            i += interval
            output = simulate_function(i)
            q.put((i, output[0][output[1].index(param_name)]))
            
            # # Create and write header to the CSV file
            # with open(f"traces/exp{exp}/{output_file}_{i}.csv", "w", encoding="utf-8") as f:
            #     f.write("iteration, x\n")
            
            # # Append data to the CSV file
            # with open(f"traces/exp{exp}/{output_file}_{i}.csv", "a", encoding="utf-8") as f:
            #     for j, x in enumerate(output[0][output[1].index(param_name)]):
            #         f.write(f"{j}, {x}\n")
        
        # # Find the smallest error
        # error_output = smallestError(f"traces/exp{exp}", calibration_file)
        q.put(None)
        error_output = future.result()
    
    # Copy the smallest error file to an answer folder
    os.makedirs("answers", exist_ok=True)
    os.makedirs("answers/part_2", exist_ok=True)
    os.makedirs("assets/part_2", exist_ok=True)
    
    # param_value = error_output[1].split("_")[-1].replace(".csv", "").replace("_", ".")
    param_value = error_output[2]
    # Create and write header to the CSV file
    with open(f"answers/part_2/{output_file}_{param_value}_{error_output[0]}.csv", "w", encoding="utf-8") as f:
        f.write("iteration, x\n")

    # Append data to the CSV file
    with open(f"answers/part_2/{output_file}_{param_value}_{error_output[0]}.csv", "a", encoding="utf-8") as f:
        for j, x in enumerate(error_output[1]):
            f.write(f"{j}, {x}\n")
    
    # # Copy the file to the answers folder
    # shutil.copyfile(f"traces/exp{exp}/{error_output[1]}", f"answers/part_2/{output_file}_{param_value}_{error_output[0]}.csv")
    
    # # delete the traces exp1 folder
    # shutil.rmtree(f"traces/exp{exp}")

    plotData(param_value, error_output[0], calibration_file, output_file, param_name)


def PIDCostFunction(max_theta: float, task_time: float):
    """Cost function to fine tune PID controller. Modifier is based on student number.
    Used student number: `{student_number}`
    theta modifer: `{a}`
    time modifier: `{b}`

    Args:
        max_theta (float): Largest angular displacement observed in radians.
        task_time (float): Time it takes to reach the set-point, with theta within 10 degrees.
        
    Returns:
        float: Cost of the PID controller.
    """
    # Higher a means more stability is required
    # Higher b means faster task time is required
    a, b = 17, 12
    return (a * max_theta) + (b * task_time)


def getTaskTime(t_list, x_list, theta_list, set_point=10, theta_bounds = 10 * np.pi / 180, accuracy=0.1):
    """Calculate task time given simulation data

    Args:
        t_list ([float]): list of times.
        x_list ([float]): list of cart displacements in meters.
        theta_list ([float]): list of angular displacements in radians.
        set_point (float, optional): Trolley needs to reach this point for task to be considered done. Defaults to 10.
        theta_bounds (float, optional): Theta must be within this angle for task to be considered done. Defaults to 10 degrees.
        accuracy (float, optional): Accuracy considered for trolley to reach set_point. Defaults to 0.1.

    Returns:
        task_time (float): Time it took for task to be considered done.
    """
    def nextPoint(x_list, set_point, accuracy):
        """Generator to get next point that crosses set_point
        """
        for i, x in enumerate(x_list):
            if (set_point + accuracy) > x > (set_point - accuracy):
                yield i, x
        raise RuntimeError("No more points")
    
    gen = nextPoint(x_list, set_point, accuracy)
    while True:
        try:
            i, _x = next(gen)
        except RuntimeError:
            return np.inf
        
        # See if pendulum is stable
        current_theta = theta_list[i]
        for theta in theta_list[i:]:
            
            if not (current_theta - theta_bounds <= theta <= current_theta + theta_bounds):
                break
        else:
            break
    return t_list[i]
            
    
def lowestCostMultiThread(q: queue.Queue, set_point=10, theta_bounds = 10 * np.pi / 180, accuracy=0.1):
    """data send by queue should be of (data, names, (p, i, d))"""

    print("Calculating smallest cost on a different thread.", flush=True)
    lowest_cost = np.inf
    pid = None

    # pop from queue
    with open("traces/costs.csv", "w") as f:
        while (trace_data := q.get()) is not None:
            t = trace_data[0][0]
            x = trace_data[0][trace_data[1].index("craneModelBlock.x")]
            theta = trace_data[0][trace_data[1].index("craneModelBlock.theta")]

            # calculate cost
            max_theta = np.absolute(theta).max()
            task_time = getTaskTime(t, x, theta, set_point, theta_bounds, accuracy)
            cost = PIDCostFunction(max_theta, task_time)
            f.write(f"{trace_data[2][0]}, {trace_data[2][2]}, {cost}, {max_theta}, {task_time}\n")
            if cost <= lowest_cost:
                lowest_cost = cost
                pid = trace_data[2]
                print(f"Current lowest cost {lowest_cost} for {pid}.")
    return lowest_cost, pid


def tunePIDControl(p_start: float = 1, i_start: float = 0, d_start: float = 10, 
                   p_interval: float = 1, i_interval: float = 0, d_interval: float = 10,
                   p_end: float = 40, i_end: float = -1, d_end: float = 500,
                   set_point=10, theta_bounds = 10 * np.pi / 180, accuracy=0.1):
    """Run simulations to fine tune PID controller.

    Args:
        p_start (float, optional): Starting value of K_p. Defaults to 1.
        i_start (float, optional): Starting value of K_i. Defaults to 0.
        d_start (float, optional): Starting value of K_d. Defaults to 10.
        p_interval (float, optional): amount to increase K_p by. Defaults to 1.
        i_interval (float, optional): amount to increase K_i by. Defaults to 0.
        d_interval (float, optional): amount to increase K_d by. Defaults to 10.
        p_end (float, optional): End value of K_p. Defaults to 40.
        i_end (float, optional): End value of K_i. Defaults to -1.
        d_end (float, optional): End value of K_d. Defaults to 500.
        set_point (float, optional): Trolley needs to reach this point for task to be considered done. Defaults to 10.
        theta_bounds (float, optional): Theta must be within this angle for task to be considered done. Defaults to 10 degrees.
        accuracy (float, optional): Accuracy considered for trolley to reach set_point. Defaults to 0.1.
    """
    cost_output = None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        q = queue.Queue()
        future = executor.submit(lowestCostMultiThread, q, set_point, theta_bounds, accuracy)

        # p-loop
        p = p_start
        while True:
            i = i_start
            
            # i-loop
            while True:
                d = d_start

                # d-loop
                while True:

                    print(f"Running simulation with parameters: {p = }, {i = }, {d = }")
                    data, names = simPIDControlModel(K_p=p, K_i=i,K_d=d,K_constant=set_point)
                    q.put((data, names, (p, i, d)))

                    d += d_interval
                    if d > d_end:
                        break
                
                i += i_interval
                if i > i_end:
                    break
            
            p += p_interval
            if p > p_end:
                break

        q.put(None)
        cost_output = future.result()
        print(f"Lowest cost: {cost_output[0]} for {cost_output[1]}")


if __name__ == "__main__":
    # runExperiment(1)
    # runExperiment(2)
    tunePIDControl()
    