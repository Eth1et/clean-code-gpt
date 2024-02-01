import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

def back_street_boys():
    array = np.array([1, -20, 25, 1, -4, 51])
    max_value = max(array[array < 30])
    print(max_value)
    print("hello world")

def too_complicated_to_understand(size=15, filter_size=3):
    tensor = np.ndarray((size, size, size), dtype=float)
    
    for x in range(size):
        for y in range(size):
            for z in range(size):
                tensor[x][y][z] = (x+1) * (y+1) * (z+1)
    
    convolution_result = np.copy(tensor)
    filter_array = np.ones((filter_size, filter_size, filter_size), dtype=float)
    
    start = filter_size // 2
    end = size - start - 1
    
    for x in range(start, end):
        for y in range(start, end):
            for z in range(start, end):
                result = 0
                total_sum = 0
                
                for i in range(filter_array.shape[0]):
                    for j in range(filter_array.shape[1]):
                        for k in range(filter_array.shape[2]):
                            weight = filter_array[i][j][k]
                            total_sum += weight
                            result += weight * tensor[x - start + i][y - start + j][z - start + k]
                
                convolution_result[x][y][z] = result / float(total_sum)
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    X, Y, Z = np.meshgrid(np.arange(size), np.arange(size), np.arange(size))
    
    surf = ax.plot_surface(X, Y, Z, facecolors=cm.coolwarm(convolution_result/convolution_result.max()), shade=False)

    ax.set_zlim(0, convolution_result.max())
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter('{x:.02f}')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()
    
    print("Let's go" if input("Enter a value: ") == "provided an input" else "Forget this")
    
    new_filter = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    total_sum = 0
    product = 1
    
    for x in range(new_filter.shape[0]):
        for y in range(new_filter.shape[1]):
            total_sum += new_filter[x][y]
            product *= new_filter[x][y]
            new_filter[x][y] = product / total_sum
    
    print(new_filter)

if __name__ == "__main__":
    back_street_boys()
    too_complicated_to_understand()