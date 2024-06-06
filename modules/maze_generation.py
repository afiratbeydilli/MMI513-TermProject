import numpy as np
import matplotlib.pyplot as plt

USE_RANDOM_FUNCTION = ""

class Graph:
    """
        Base class that will be the foundation of the Maze.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.vertices = self.determine_vertices()  # [(x, y), ...]
        self.edges = self.determine_edges()  # [ ((x1, y1), (x2, y2)), ...]

    def determine_vertices(self):
        vertices = []
        for x_coordinate in range(self.width):
            for y_coordinate in range(self.height):
                vertices.append((x_coordinate, y_coordinate))

        return vertices

    def copy(self):
        new_graph = Graph(self.width, self.height)
        return new_graph

    # Will be used to determine the edges.
    def neighbors(self, x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [(x + dx, y + dy) for dx, dy in directions
                if 0 <= x + dx < self.width and 0 <= y + dy < self.height]

    def determine_edges(self):
        edges = []

        for vertex in self.vertices:
            neighbors_of_vertex = self.neighbors(vertex[0], vertex[1])
            for neighbor in neighbors_of_vertex:
                edge = (vertex, neighbor)
                reverse_edge = (neighbor, vertex)
                if (edge not in edges) and (reverse_edge not in edges):
                    edges.append(edge)
        return edges

    def random_vertex(self):
        # USE_RANDOM_FUNCTION
        randomint = np.random.randint(0, len(self.vertices))
        return self.vertices[randomint]

    @staticmethod
    def ends(edge):
        assert isinstance(edge, tuple)
        assert isinstance(edge[0], tuple) and isinstance(edge[1], tuple)
        return {edge[0], edge[1]}

class Maze(Graph):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.walls = self.determine_walls()  # Subset of edges
        self.available_edges = None  # Initially, all edges are intact.
        self.available_path = None  # Initially, there is no path to navigate.

    def copy(self):
        new_maze = Maze(self.width, self.height)
        return new_maze

    def determine_walls(self):
        walls = []
        for e in self.edges:
            vec = np.array([e[1][0] - e[0][0], e[1][1] - e[0][1]])  # Vector from point1 to point2
            ort = np.array([-vec[1], vec[0]])  # Orthogonal vector to vec
            olen = np.linalg.norm(ort)  # Length of the orthogonal vector
            ort = ort / olen  # Normalize the orthogonal vector
            midpoint = np.array([(e[1][0] + e[0][0]) / 2, (e[1][1] + e[0][1]) / 2])  # Midpoint of the edge
            startpoint = midpoint - ort / 2  # Start point for the wall line (orthogonal shift)
            endpoint = midpoint + ort / 2  # End point for the wall line (orthogonal shift)
            walls.append(((startpoint[0], endpoint[0]), (startpoint[1], endpoint[1])))
        return walls

    def plot_maze(self, show_vertices=True):

        plt.rcParams['figure.figsize'] = [15, 15]
        fig, ax = plt.subplots()

        for wall in self.walls:
            # Plot the wall as a thick black line orthogonal to the original edge
            ax.plot(wall[0], wall[1], 'k', linewidth=10)

        if show_vertices:
            # Plot vertices
            for vertex in self.vertices:
                ax.plot(float(vertex[0]), float(vertex[1]), 'ro')  # Red circle markers for vertices

        # Arrange the tick distances
        ax.set_xticks(range(max(v[0] for v in self.vertices) + 1))
        ax.set_yticks(range(max(v[1] for v in self.vertices) + 1))

        # Show the plot
        plt.show()

    @staticmethod
    def random_wall(walls):
        # USE_RANDOM_FUNCTION
        list_walls = list(walls)
        randomint = np.random.randint(0, len(list_walls))
        return list_walls[randomint]

    def prims_algorithm(self):
        assert len(self.vertices) > 0 and len(self.edges) > 0

        # In this function, edges will be used as walls, and the modification will be done at the very end.
        W = set(self.edges.copy())
        C = set()  # Visited cells
        L = set()  # Set of walls/edges to check out, initially empty.

        c = self.random_vertex()  # Select a random cell (vertex) and mark it as visited
        C.add(c)

        for wall in W:
            if c in self.ends(wall):
                L.add(wall)  # Add

        flag = (len(L) > 0)
        while flag:
            l = self.random_wall(L)

            if len(self.ends(l).intersection(C)) <= 1:
                for node in l:
                    C.add(node)  # Will add the not-added node only, and will be marked as visited.

                W.remove(l)  # Remove the wall

                for w in W:
                    if len(self.ends(w).intersection(self.ends(l))) > 0:
                        if (w in L) is False:
                            L.add(w)

            L.remove(l)
            flag = len(L) > 0  # Flag update

        self.edges = list(W)
        self.walls = self.determine_walls()
        return self

    def update_maze(self):
        return self.prims_algorithm()

    def determine_available_edges(self):
        """
            Based on the walls variable and copy functions, determines the edges
            that are available if any agent wants to walk through.
        """
        self.available_edges = []  # Reset this variable each time this method is called
        new_intact_maze = Maze(self.width, self.height)
        for edge in new_intact_maze.edges:
            if edge not in self.edges:
                self.available_edges.append(edge)

def maze_generation():
    m = Maze(3, 3)
    # m.plot_maze(False)
    m.update_maze()
    m.determine_available_edges()
    print(len(m.available_edges))
    m.plot_maze(False)

