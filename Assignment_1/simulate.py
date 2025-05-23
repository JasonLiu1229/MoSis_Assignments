# This file contains example Python code to demonstrate the simulation of the newtonCooling Modelica model
# You need os package to execute commands in shell
import os

# ´os.system()´ does not wait until process is finished in linux, so use subprocess instead
import subprocess

# This function simulates the model, once, with the given parameters, by executing through a shell command.
# It reads the results by calling the readMat function and displays a graph of the Temperature versus Time by calling the plotData function
# This function takes parameter values of the newtonCoolingWithTypes model.
def singleSimulation(m=0.2, M=10, r=1, d_p=0.5, d_c=2, plot=False):
    """Single simulation function

    Args:
        m (float, optional): mass of pendulum. Defaults to 0.2.
        M (int, optional): mass of trolley. Defaults to 10.
        r (int, optional): length of pendulum rope. Defaults to 1.
        d_p (float, optional): damping factor of pendulum. Defaults to 0.5.
        d_c (int, optional): damping factor of motion of cart. Defaults to 2.
        plot (bool, optional): plot the data. Defaults to False.

    Returns:
        tuple: data and names
    """
    # Create the string command that will be executed to execute the Modelica model
    # The command is structured as './<executable name> -override <param1 name>=<param1 value>, <param2 name>=<param2 value>..'
    simulationCommand=f'./CraneModel -override m={m},M={M},r={r},d_p={d_p},d_c={d_c}'
    # Assuming that your shell is focused on the example/ directory, you should change directory to the one actually containing the executable. This directory usually has the same name as the Modelica file name.
    # Create the corresponding string command and execute it.
    directoryChangeCommand='cd /GantryControlSystem.CraneModel'
    os.chdir('GantryControlSystem.CraneModel')
    # Simulate the model
    os.system(simulationCommand)
    # Obtain the variable values by reading the MAT-file    
    [names, data] = readMat('CraneModel_res.mat')
    # Create a plot
    if plot:
        openDataPlot(data[names.index('time')],data[names.index('theta')],'time (s)','theta (rad)')
    # Return the data and names
    return (data, names)
    

def singleSimExpOne(d_c=2, M=10, r=1):
    """Single simulation function

    Args:
        d_c (float, optional): damping factor of motion of cart. Defaults to 2.
        M (int, optional): mass of trolley. Defaults to 10.
        r (int, optional): length of pendulum rope. Defaults to 1.

    Returns:
        tuple: data and names
    """
    try:
        # Change directory to the folder where the CraneModelExpOne executable is located
        os.chdir('GantryControlSystem.CraneModelExpOne')
        
        # Create the list of arguments that will be executed
        simulationCommand = [
            './CraneModelExpOne',
            '-override',
            f'M={M},r={r},d_c={round(d_c, 6)}'
        ]
        
        # Simulate the model using subprocess without shell=True
        subprocess.run(simulationCommand)
        
        # Obtain the variable values by reading the MAT-file
        [names, data] = readMat('CraneModelExpOne_res.mat')
    
    finally:
        # Change back to the parent directory
        os.chdir('..')

    # Return the data and names
    return (data, names)


def singleSimExpTwo(d_p=0.5, m=0.2, r=1):
    """Single simulation function, exactly the same as `singleSimExpOne`, except a different model.

    Args:
        d_p (float, optional): damping factor of motion of pendulum. Defaults to 0.5.
        m (float, optional): mass of pendulum / container. Defaults to 0.2.
        r (float, optional): length of pendulum rope. Defaults to 1.

    Returns:
        tuple: data and names
    """
    try:
        # Change directory to the folder where the CraneModelExpOne executable is located
        os.chdir('GantryControlSystem.CraneModelExpTwo')
        
        # Create the list of arguments that will be executed
        simulationCommand = [
            './CraneModelExpTwo',
            '-override',
            f'm={m},r={r},d_p={round(d_p, 6)}'
        ]
        
        # Simulate the model using subprocess without shell=True
        subprocess.run(simulationCommand)
        
        # Obtain the variable values by reading the MAT-file
        [names, data] = readMat('CraneModelExpTwo_res.mat')
    
    finally:
        # Change back to the parent directory
        os.chdir('..')

    # Return the data and names
    return (data, names)


def simPIDControlModel(*, K_p=1, K_i=1, K_d=1, K_constant=20, M=10, m=0.2, r=1):
    """Single simulation function

    Args:
        K_p (float, optional): proportional gain. Defaults to 1.
        K_i (float, optional): integral gain. Defaults to 1.
        K_d (float, optional): derivative gain. Defaults to 1.
        K_constant (float, optional): constant gain. Defaults to 1.
        M (float, optional): Mass of the cart. Defaults to 10.
        m (float, optional): Mass of the pendulum. Defaults to 0.2.
        r (float, optional): Length of the rope in meters. Defaults to 1.
        
    Returns:
        tuple: data and names
    """
    try:
        # Change directory to the folder where the CraneModelExpOne executable is located
        os.chdir('GantryControlSystem.PIDControlLoopModel')
        
        # Create the list of arguments that will
        simulationCOmmand = [
            './PIDControlLoopModel',
            '-override',
            f'pIDControllerBlock.K_p={K_p},pIDControllerBlock.K_i={K_i},pIDControllerBlock.K_d={K_d},K_constant={K_constant}'
            f',craneModelBlock.M={M},craneModelBlock.m={m},craneModelBlock.r={r}'
        ]
        
        # Simulate the model using subprocess without shell=True
        subprocess.run(simulationCOmmand)
        
        # Obtain the variable values by reading the MAT-file
        [names, data] = readMat('PIDControlLoopModel_res.mat')
        
    finally:
        # Change back to the parent directory
        os.chdir('..')
        
    # Return the data and names
    return (data, names)
        

# You need scipy package to read MAT-files
from scipy import io
# Reuse this exact function to read MAT-file data.
# matFileName is the name of the MAT-file generated on execution of a Modelica executable
# The output is [names, data] where names is an array of strings which are names of variables, data is an array of values of the associated variable in the same order
def readMat(matFileName):
    dataMat =  io.loadmat(matFileName)
    names = [''] * len(dataMat['name'][0])
    data = [None] * len(names)
    # Check if the matrix of metadatas are transposed.
    if dataMat['Aclass'][3] == 'binTrans':
        # If the matrix of  matadata needs to be transposed, the names nead to be read from each string
        for x in range(len(dataMat['name'])):
            for i in range(len(dataMat['name'][x])):
                if dataMat['name'][x][i] != '\x00':
                    names[i] = names[i] + dataMat['name'][x][i]
        # If the matrix of metadata needs to be transposed, the index of variable trace needs to be read in a transposed fashion
        for i in range(len(names)):
            # If it is a variable, read the whole array
            if (dataMat['dataInfo'][0][i] == 0) or (dataMat['dataInfo'][0][i] == 2):
                data[i] = dataMat['data_2'][dataMat['dataInfo'][1][i]-1]
            # If it is a parameter, read only the first value
            elif dataMat['dataInfo'][0][i] == 1:
                data[i] = dataMat['data_1'][dataMat['dataInfo'][1][i]-1][0]
    else:
        # If the matrix of metadata need not be transposed, the names can be read directly as individual strings
        names = dataMat['name']
        # If the matrix of metadata need not be transposed, the index of variable trace needs to be read directly
        for i in range(len(names)):
            # If it is a variable, read the whole array
            if (dataMat['dataInfo'][i][0] == 0) or (dataMat['dataInfo'][i][0] == 2):
                data[i] = dataMat['data_2'][dataMat['dataInfo'][i][1]-1]
            # If it is a parameter, read only the first value
            elif dataMat['dataInfo'][i][0] == 1:
                data[i] = dataMat['data_1'][dataMat['dataInfo'][i][1]-1][0]
    # Return the names of variables, and their corresponding values
    return [names,data]

# You need matplotlib to plot
from matplotlib import pyplot
# This function plots the data from the simulation.
# xdata is x-axis data
# ydata is corresponding y-axis data
# xLabel is the string label value to be displayed in the plot for the x axis
# yLabel is the string label value to be displayed in the plot for the y axis
def openDataPlot(xdata, ydata, xLabel, yLabel):
    figure, axis = pyplot.subplots()
    axis.plot(xdata, ydata)
    pyplot.xlabel(xLabel)
    pyplot.ylabel(yLabel)
    pyplot.show()

# "function" that calls the single simulation function from shell. In your code, this function call should be in a loop ove the combinations of parameters.
if __name__ == "__main__":
    singleSimulation()

# The follwing function is an alternative way of executing/simulating the Modelica model using the OMPython package. This method is not recommended.
# from OMPython import OMCSessionZMQ, ModelicaSystem
# def singleSimulationOMPython(T_inf=298.15, T0=363.15, h=0.7, A=1.0, m=0.1, c_p=1.2):
#     omc = OMCSessionZMQ()
#     model = ModelicaSystem('example.mo','NewtonCoolingWithTypes')
#     model.buildModel('T')
#     print('Performing simulation: Ambient Temp.:',str(T_inf),
#                                ', Initial Temp.:',str(initTemp),
#                                ', Convection Coeff.:',str(h),
#                                ', Area:',str(A),
#                                ', Mass:',str(m),
#                                ', Specific Heat:',str(Cp))
#
#     model.setSimulationOptions(["stepSize=0.01",
#                                 "tolerance=1e-9",
#                                 "startTime=0",
#                                 "stopTime=10"])
#     model.setParameters(['T_inf='+str(T_inf),
#                          'T0='+str(T0),
#                          'h='+str(h),
#                          'A='+str(A),
#                          'm='+str(m),
#                          'c_p='+str(c_p)])
#     model.simulate()
#     samples = model.getSolutions(["time", "T"])
#     openDataPlot([samples[0]],[samples[1]],'time (seconds)','temperature (C)')
