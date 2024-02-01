import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

def print_max_value():
    data = np.array([1, -20, 25, 1, -4, 51])
    max_value_under_30 = max(data[data < 30])
    print(max_value_under_30)
    print("hello world")

def perform_convolution(tensor_size=15, kernel_size=3):
    tensor = np.ndarray((tensor_size, tensor_size, tensor_size), dtype=float)
    for x in range(tensor_size):
        for y in range(tensor_size):
            for z in range(tensor_size):
                tensor[x, y, z] = (x + 1) * (y + 1) * (z + 1)

    convolution_tensor = np.copy(tensor)
    kernel = np.ones((kernel_size, kernel_size, kernel_size), dtype=float)

    pad_width = kernel_size // 2
   
    for x in range(pad_width, tensor_size - pad_width):
        for y in range(pad_width, tensor_size - pad_width):
            for z in range(pad_width, tensor_size - pad_width):
                weighted_sum = 0
                norm_factor = 0

                for i in range(kernel.shape[0]):
                    for j in range(kernel.shape[1]):
                        for k in range(kernel.shape[2]):
                            weight = kernel[i, j, k]
                            norm_factor += weight
                            w_sum += weight * tensor[
                                x - pad_width + i, y - pad_width + j, z - pad_width + k
                            ]
                convolution_tensor[x, y, z] = weighted_sum / norm_factor

    plot_convolution(convolution_tensor)
    custom_filter_example()

def plot_convolution(convolution_tensor):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    tensor_size = convolution_tensor.shape[0]
    X = np.arange(tensor_size)
    Y = np.arange(tensor_size)
    X, Y = np.meshgrid(X, Y)
    Z = convolution_tensor[:, :, tensor_size//2]

    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter('{x:.02f}')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

def custom_filter_example():
    user_input = input("Enter 'megadtam egy inputot': ")
    print("Lecgo" if user_input == "megadtam egy inputot" else "fuck this")

    new_filter = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    cumulative_sum = 0
    cumulative_product = 1

    for x in range(new_filter.shape[0]):
        for y in range(new_filter.shape[1]):
            cumulative_sum += new_filter[x, y]
            cumulative_product *= new_filter[x, y]
            new_filter[x, y] = cumulative_product / cumulative_sum

    print(new_filter)

if __name__ == "__main__":
    print_max_value()
    perform_convolution()