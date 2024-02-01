import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

def find_max_value_below_30():
    array = np.array([1, -20, 25, 1, -4, 51])
    max_value = max(array[array < 30])
    print(max_value)
    print("hello world")

def perform_3d_convolution(size=15, filter_size=3):
    tensor = np.zeros((size, size, size), dtype=float)
    
    for x in range(size):
        for y in range(size):
            for z in range(size):
                tensor[x][y][z] = (x + 1) * (y + 1) * (z + 1)
                
    convolution_result = np.copy(tensor)
    filter = np.ones((filter_size, filter_size, filter_size), dtype=float)
    
    start = filter_size // 2
    end = size - start - 1
                
    for x in range(start, end):
        for y in range(start, end):
            for z in range(start, end):
                result = 0
                divisor = 0
                
                for i in range(filter_size):
                    for j in range(filter_size):
                        for k in range(filter_size):
                            weight = filter[i][j][k]
                            divisor += weight
                            result += weight * tensor[x - start + i][y - start + j][z - start + k]
                
                convolution_result[x][y][z] = result / float(divisor)
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    X, Y, Z = np.meshgrid(range(size), range(size), range(size))
    surf = ax.plot_surface(X, Y, Z, facecolors=convolution_result, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter('{x:.02f}')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()
    
    user_input = input("Enter a message: ")
    print("Lecgo" if user_input == "megadtam egy inputot" else "fuck this")
    
    new_filter = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    divisor = 0
    product = 1
    
    for x in range(new_filter.shape[0]):
        for y in range(new_filter.shape[0]):
            divisor += new_filter[x][y]
            product *= new_filter[x][y]
            new_filter[x][y] = product / divisor
            
    print(new_filter)

if __name__ == "__main__":
    find_max_value_below_30()
    perform_3d_convolution()