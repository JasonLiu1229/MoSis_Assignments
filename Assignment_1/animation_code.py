#!/usr/bin/env python
__author__ = "Rakshit Mittal"
__copyright__ = "Copyright 2024, MSDL, University of Antwerp, Belgium"
__credits__ = ["Hans Vangheluwe", "Joost Mertens"]
__license__ = "MIT"
__maintainer__ = "Rakshit Mittal"
__email__ = "rakshit.mittal@uantwerpen.be"
"""
This Python module is used to animate the gantry system Modelica model based on its solution from the 
executed Modelica-compiled code.
"""
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

matplotlib.use('TkAgg')

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


def animate_gantry_system(x_array, theta_array, length, interval=1):
    """
    Create an animation of a gantry system based on arrays of x positions and pendulum angles theta.

    :param x_array: Array of cart positions along the x-axis.
    :param theta_array: Array of pendulum angles (in radians).
    :param length: optional, Length of the pendulum (rope), default is 1.0.
    :param interval : optional, Delay between frames in milliseconds, default is 1ms.
    """
    # Set ambiguous cart width
    cart_width = 0.4
    cart_height = 0.2

    # Calculate figure limits
    x_min = np.min(x_array) - 1.0
    x_max = np.max(x_array) + 1.0
    y_min = -length - 1.0
    y_max = cart_height + 1.0

    # Create figure of appropriate size
    fig, ax = plt.subplots()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect('equal')
    ax.grid()

    # Draw rails
    ax.plot([x_min, x_max], [0, 0], 'k--', lw=2)

    # Initialize cart
    cart = Rectangle((x_array[0] - cart_width / 2, 0), cart_width, cart_height, fc='blue', ec='black')
    ax.add_patch(cart)

    # Initialize pendulum line and bob
    pendulum_line, = ax.plot([], [], lw=2, c='red')
    pendulum_bob, = ax.plot([], [], 'o', c='black')

    def init():
        # Initialize cart position
        cart.set_xy((x_array[0] - cart_width / 2, 0))

        # Calculate initial pendulum end point
        pendulum_x = x_array[0] + length * np.sin(theta_array[0])
        pendulum_y = -length * np.cos(theta_array[0])

        # Initialize pendulum line
        pendulum_line.set_data([x_array[0], pendulum_x], [0, pendulum_y])

        # Initialize pendulum bob
        pendulum_bob.set_data([pendulum_x], [pendulum_y])  # Wrap in lists

        return cart, pendulum_line, pendulum_bob

    def animate(i):
        # Update cart position
        cart.set_xy((x_array[i] - cart_width / 2, 0))

        # Calculate pendulum end point
        pendulum_x = x_array[i] + length * np.sin(theta_array[i])
        pendulum_y = -length * np.cos(theta_array[i])

        # Update pendulum line
        pendulum_line.set_data([x_array[i], pendulum_x], [0, pendulum_y])

        # Update pendulum bob
        pendulum_bob.set_data([pendulum_x], [pendulum_y])  # Wrap in lists

        return cart, pendulum_line, pendulum_bob

    ani = animation.FuncAnimation(fig, animate, frames=len(x_array), init_func=init, blit=True, interval=interval)

    plt.show()

def plot_graph(x_data, y_data, x_label, y_label, title):
    """Plot data of given datasets

    Args:
        x_data (list): List of x-axis data
        y_data (list): List of y-axis data
        x_label (string): Label for x-axis
        y_label (string): Label for y-axis
        title (string): Title of the plot
    """
    os.makedirs("assets/", exist_ok=True)
    os.makedirs("assets/part_4", exist_ok=True)
    
    plt.figure()
    plt.plot(x_data, y_data, label=y_label)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    
    title_name = title.replace(" ", "_")
    
    plt.legend()
    plt.grid(True)
    
    plt.savefig(f"assets/part_4/{title_name}.png")

# Example usage:
if __name__ == "__main__":
    # Sample data for x and theta
    # t = np.linspace(0, 10, 200)
    # x = 2 * np.sin(0.5 * t)  # Example cart positions
    # theta = 0.2 * np.sin(2 * t)  # Example pendulum angles (in radians)

    from simulate import simPIDControlModel

    data, names = simPIDControlModel(K_p=16, K_i=0, K_d=10)
    # 240.68844433057455 for (16, 0, 10)
    x = data[names.index("craneModelBlock.x")]
    theta = data[names.index("craneModelBlock.theta")]
    
    plot_graph(range(len(x)), x, "Time", "Cart Position", "Cart Position vs Time")
    plot_graph(range(len(theta)), theta, "Time", "Pendulum Angle", "Pendulum Angle vs Time")

    # Call the animation function with sample data
    # NOTE: if max(x) is very big compared to the cart, the pendulum will not be visible
    # this can somewhat be fixed by replacing the equal in `ax.set_aspect('equal')` with auto inside the function, but it will look somewhat wonky
    # You can also divide x to make it smaller
    animate_gantry_system(x, theta, length=1, interval=0.004)
