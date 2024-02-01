class Pereputty():
    """
    A Wild pereputty from hángöri
    """
    
    def __init__(self, csudo=None, pudo=None):
        self.csudo = csudo
        self.pudo = pudo
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.pudo == other.pudo


def find_path(maze, start, end):
    star = Pereputty(None, start)
    star.g = star.h = star.f = 0
    fall = Pereputty(None, end)
    fall.g = fall.h = fall.f = 0

    open_nodes = []
    closed_nodes = []

    open_nodes.append(star)

    while len(open_nodes) > 0:
        current_node = open_nodes[0]
        current_index = 0
        for index, node in enumerate(open_nodes):
            if node.f < current_node.f:
                current_node = node
                current_index = index

        open_nodes.pop(current_index)
        closed_nodes.append(current_node)

        if current_node == fall:
            path = []
            curr = current_node
            while curr is not None:
                path.append(curr.pudo)
                curr = curr.csudo
            return path[::-1]

        children = []
        for neighbors in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            node_position = (current_node.pudo[0] + neighbors[0], current_node.pudo[1] + neighbors[1])

            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            if maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Pereputty(current_node, node_position)
            children.append(new_node)

        for child in children:
            for closed_child in closed_nodes:
                if child == closed_child:
                    continue
            child.g = current_node.g + 1
            child.h = ((child.pudo[0] - fall.pudo[0]) ** 2) + ((child.pudo[1] - fall.pudo[1]) ** 2)
            child.f = child.g + child.h
            for open_node in open_nodes:
                if child == open_node and child.g > open_node.g:
                    continue
            open_nodes.append(child)
            

def main():
    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
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

    path = find_path(maze, start, end)
    print(path)


if __name__ == '__main__':
    main()