from simulate import singleSimExpOne

import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt

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
    smallest_error = None
    smallest_error_file = None
    for file in os.listdir(trace_dir):
        error = sumSquaredError(os.path.join(trace_dir, file), calibration_file)
        if smallest_error is None or error < smallest_error:
            smallest_error = error
            smallest_error_file = file
    
    return (smallest_error, smallest_error_file)

def runExperimintOne(interval=5.00/10000):
    """Run experiment one. Copy the trace file with the smallest error to the answers folder.

    Args:
        interval (float, optional): The interval to increment d_c by. Defaults to 5.00/10000.
        
    Returns:
        None
    """
    # Ensure the 'traces' directory exists and create the 'exp1' subdirectory
    os.makedirs('traces', exist_ok=True)
    os.makedirs('traces/exp1', exist_ok=True)
    
    i = 0.00
    k = 0
    while i < 5.00:
        print("Running simulation ", k)
        k += 1
        i += interval
        output = singleSimExpOne(d_c=i)
        
        # Create and write header to the CSV file
        with open(f"traces/exp1/experiminent_one_traces_{i}.csv", "w", encoding="utf-8") as f:
            f.write("iteration, x\n")
        
        # Append data to the CSV file
        with open(f"traces/exp1/experiminent_one_traces_{i}.csv", "a", encoding="utf-8") as f:
            for j, x in enumerate(output[0][output[1].index("x")]):
                f.write(f"{j}, {x}\n")
    
    # Find the smallest error
    error_output = smallestError("traces/exp1", "calibration_data_d_c.csv")
    
    # Copy the smallest error file to an answer folder
    os.makedirs("answers", exist_ok=True)
    os.makedirs("answers/exp1", exist_ok=True)
    os.makedirs("assets/part_2", exist_ok=True)
    
    d_c_value = error_output[1].split("_")[-1].replace(".csv", "").replace("_", ".")
    # Copy the file to the answers folder
    shutil.copyfile(f"traces/exp1/{error_output[1]}", f"answers/exp1/experiminent_one_traces_{d_c_value}_{error_output[0]}.csv")
    
    # delete the traces exp1 folder
    shutil.rmtree("traces/exp1")
    
    # Plot the data
    data1 = pd.read_csv(f"answers/exp1/experiminent_one_traces_{d_c_value}_{error_output[0]}.csv")
    data2 = pd.read_csv("calibration_data_d_c.csv")
    
    extracted_data1 = data1.iloc[:, 1]
    extracted_data2 = data2.iloc[:, 1]
    
    plt.plot(extracted_data1, label="Model Output", color="red")
    plt.plot(extracted_data2, label="Calibration Data", color="blue")
    
    plt.xlabel("Iteration")
    plt.ylabel("d_c")
    
    plt.legend()
    plt.grid(True)
    
    plt.savefig(f"assets/part_2/experiminent_one_traces_{d_c_value}_{error_output[0]}.png")
    
    plt.figure()
    plt.plot(extracted_data1, label="Model Output", color="red")
    plt.xlabel("Iteration")
    plt.ylabel("d_c")
    
    plt.legend()
    plt.grid(True)
    
    plt.savefig(f"assets/part_2/experiminent_one_traces_{d_c_value}_{error_output[0]}_Model.png")
    
    plt.figure()
    plt.plot(extracted_data2, label="Calibration Output", color="blue")
    plt.xlabel("Iteration")
    plt.ylabel("d_c")
    
    plt.legend()
    plt.grid(True)
    
    plt.savefig(f"assets/part_2/experiminent_one_traces_{d_c_value}_{error_output[0]}_Cali.png")

            
def runExperimintTwo():
    pass

if __name__ == "__main__":
    runExperimintOne()
    # runExperimintTwo()
