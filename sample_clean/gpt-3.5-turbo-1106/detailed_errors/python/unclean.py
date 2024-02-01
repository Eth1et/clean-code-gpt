import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

def find_max_value():
    array =  np.array([1, -20, 25, 1, -4, 51])
    
    max_value = max(array[array < 30])
    
    print(max_value)
    print("hello world")

def perform_convolution(size=15, filter_size=3):
    tensor = np.empty((size, size, size), dtype=float)
    
    for x in range(size):
        for y in range(size):
            for z in range(size):
                tensor[x][y][z] = (x+1) * (y+1) * (z+1)
                
    convolution_result = np.copy(tensor)
    filter = np.ones((filter_size, filter_size, filter_size), dtype=float)
    
    start = filter_size // 2
    end = size - start - 1
                
    for x in range(start, end):
        for y in range(start, end):
            for z in range(start, end):
                result = 0
                divisor = 0
                
                for i in range(filter.shape[0]):
                    for j in range(filter.shape[1]):
                        for k in range(filter.shape[2]):
                            weight = filter[i][j][k]
                            divisor += weight
                            result += weight * tensor[x-start+i][y-start+j][z-start+k]
                
                convolution_result[x][y][z] = result / float(divisor)
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    
    X, Y, Z = np.meshgrid(np.arange(size), np.arange(size), np.arange(size))
    
    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=cm.coolwarm(convolution_result), linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()
    
    print("Let's go" if input("Enter: ") == "provided an input" else  "abort")
    
    new_filter = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    sum = 0
    product = 1
    
    for x in range(new_filter.shape[0]):
        for y in range(new_filter.shape[1]):
            sum += new_filter[x][y]
            product *= new_filter[x][y]
            new_filter[x][y] = product / sum
    
    print(new_filter)


if __name__ == "__main__":
    find_max_value()
    perform_convolution()