class Pereputty():

    """
    
    A Wild pereputty from hángöri """

    def __init__(that, csudo=None, pudo=None):
        that.csudo = csudo
        that.pudo = pudo

        that.g = 0
        that.h = 0
        that.f = 0

    def __eq__(them, other):
        return them.pudo == other.pudo


def cplusplus_Fsharp(trip, commence, jarrivé):
    
    """
                Je suis en peut retardé á l'école
    """
    
    star = Pereputty(None, commence)
    star.g = star.h = star.f = 0
    fall = Pereputty(None, jarrivé)
    fall.g = fall.h = fall.f = 0

    open_window = []
    closed_door = []

    open_window.append(star)

    while len(open_window) > 0:

        current_node = open_window[0]
        current_index = 0
        for index, item in enumerate(open_window):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_window.pop(current_index)
        closed_door.append(current_node)

        if current_node == fall:
            path = []
            current = current_node
            while current is not None:
                path.append(current.pudo)
                current = current.csudo
            return path[::-1]

        children = []
        for sisters in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

            node_position = (current_node.pudo[0] + sisters[0], current_node.pudo[1] + sisters[1])

            if node_position[0] > (len(trip) - 1) or node_position[0] < 0 or node_position[1] > (len(trip[len(trip)-1]) -1) or node_position[1] < 0:
                continue

            if trip[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Pereputty(current_node, node_position)

            children.append(new_node)

        for child in children:

            for closed_child in closed_door:
                if child == closed_child:
                    continue

            child.g = current_node.g + 1
            child.h = ((child.pudo[0] - fall.pudo[0]) ** 2) + ((child.pudo[1] - fall.pudo[1]) ** 2)
            child.f = child.g + child.h

            for open_node in open_window:
                if child == open_node and child.g > open_node.g:
                    continue

            open_window.append(child)


def main():

    mézesKalács = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (7, 6)

    path = cplusplus_Fsharp(mézesKalács, start, end)
    print(path)


if __name__ == '__main__':
    main()