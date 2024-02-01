import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

def find_max_value_below_threshold():
    numbers = np.array([1, -20, 25, 1, -4, 51])
    max_value_below_threshold = max(numbers[numbers < 30])
    print(max_value_below_threshold)
    print("hello world")

def perform_3d_convolution(size=15, filter_size=3):
    tensor = np.empty((size, size, size), dtype=float)
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
                total_weight = 0

                for i in range(filter_size):
                    for j in range(filter_size):
                        for k in range(filter_size):
                            weight = filter[i][j][k]
                            total_weight += weight
                            result += weight * tensor[x - start + i][y - start + j][z - start + k]

                convolution_result[x][y][z] = result / float(total_weight)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    X, Y, Z = np.meshgrid(np.arange(size), np.arange(size), np.arange(size))
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=cm.coolwarm(convolution_result), linewidth=0, antialiased=False, shade=False)
    
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter('{x:.02f}')
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()
    
    user_input = input("Enter a value: ")
    print("Lecgo" if user_input == "megadtam egy inputot" else "fuck this")
    
    new_filter = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    total_sum = 0
    total_product = 1
    
    for x in range(new_filter.shape[0]):
        for y in range(new_filter.shape[1]):
            total_sum += new_filter[x][y]
            total_product *= new_filter[x][y]
            new_filter[x][y] = total_product / total_sum
            
    print(new_filter)

if __name__ == "__main__":
    find_max_value_below_threshold()
    perform_3d_convolution()