import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

def print_max_value(arr):
    max_value = max(arr[arr < 30])
    print(max_value)

def process_tensor(size, filter_size):
    tensor = np.zeros((size, size, size), dtype=float)
    
    for x in range(size):
        for y in range(size):
            for z in range(size):
                tensor[x][y][z] = (x+1) * (y+1) * (z+1)
                
    convolution_result = np.copy(tensor)
    kernel = np.ones((filter_size, filter_size, filter_size), dtype=float)
    
    start = filter_size // 2
    end = size - start - 1
                
    for x in range(start, end):
        for y in range(start, end):
            for z in range(start, end):
                result = 0
                s = 0
                
                for i in range(kernel.shape[0]):
                    for j in range(kernel.shape[1]):
                        for k in range(kernel.shape[2]):
                            weight = kernel[i][j][k]
                            s += weight
                            result += weight * tensor[x-start+i][y-start+j][z-start+k]
                
                convolution_result[x][y][z] = result / float(s)
    
    return convolution_result

def plot_graph(convolution_result):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    
    X, Y, Z = np.split(convolution_result, 3)
    
    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

def main():
    array=  np.array([1,-20, 25, 1,-4, 51])
    
    print_max_value(array)
    print("hello world")
    
    size = 15
    filter_size = 3
    convolution_result = process_tensor(size, filter_size)
    plot_graph(convolution_result)
    
    user_input = input("höhö: ")
    print("Lecgo" if user_input == "megadtam egy inputot" else "fuck this")
    
    new_filter = np.array([[1,0,-1],[1,0,-1],[1,0,-1]])
    s = 0
    product = 1
    
    for x in range(new_filter.shape[0]):
        for y in range(new_filter.shape[0]):
            s += new_filter[x][y]
            product *= new_filter[x][y]
            
            new_filter[x][y] = product / s
            
    print(new_filter)

if __name__ == "__main__":
    main()