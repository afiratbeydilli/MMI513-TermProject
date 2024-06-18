import matplotlib.pyplot as plt
inf = float('inf')

class PathUtils:

    def __init__(self):
        self.can_be_finished = False

    def plotPath(self, vertices, edges, start, end):  # Plots the calculated path from the start and end vertices
        x, y = [], []
        for v in vertices:
            x.append(v[0])
            y.append(v[1])
            plt.scatter(x, y)
            plt.axis('equal')  # Equal aspect ratio
        for e in edges:
            plt.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], 'k')
            plt.text(start[0], start[1], 'Start', verticalalignment='bottom', horizontalalignment='right', color='blue')
            plt.text(end[0], end[1], 'End', verticalalignment='bottom', horizontalalignment='right', color='blue')
            # Specify start and end vertices

    # Heuristic measure takes the max of the vertical
    # and horizontal distance to goal vertex
    def h(self, v, r):
        return max(abs(r[0] - v[0]), abs(r[1] - v[1]))

    # Weight of and edge in manhattan metric
    def manhattanDistance(self, v, u):
        return abs(v[0] - u[0]) + abs(v[1] - u[1])

    # Return the vertices that can be accessed from the selected vertice, similar to neighbour
    def getSuccessors(self, selectedVertice, edges, vertices):
        successorList = []
        for e in edges:
            if e[0] == selectedVertice and e[1] in vertices:
                if not (e[1] in successorList):
                    successorList.append(e[1])
            elif e[1] == selectedVertice and e[0] in vertices:
                if not (e[0] in successorList):
                    successorList.append(e[0])
        return successorList

    def calculatePathFromMapping(self, res, s, r):  # Calculate the path from the result of A* or Dijkstra Algorithm

        finished = False
        prev = res[r]
        steps = [r, prev]
        while prev != s:
            prev = res[prev]
            steps.append(prev)

        travelledEdges = []
        for i in range(len(steps) - 1):
            travelledEdges.append(((steps[i]), (steps[i + 1])))
        travelledEdges.reverse()
        steps.reverse()

        if self.can_be_finished:
            if (len(steps) == 1 or len(travelledEdges) == 1) and res[r] == s:
                finished = True
            else:
                self.can_be_finished = False

        elif (len(steps) == 1 or len(travelledEdges) == 1) and res[r] == s:
            self.can_be_finished = True

        return steps, travelledEdges, finished

class WeightMatrix:
    """
        A matrix class to store the distance between vertices. This class implements g(s->r) function in
        A-Star & distance function in Dijkstra
    """
    def __init__(self, vertices):
        self.vertices = vertices
        self.matrix = []
        for i in range(len(vertices)):
            self.matrix.append([inf]*len(vertices))

    def __getitem__(self, index):
        s, v = index
        return self.matrix[self.vertices.index(s)][self.vertices.index(v)]

    def __setitem__(self, index, value):
        s, v = index
        self.matrix[self.vertices.index(s)][self.vertices.index(v)] = value

class AStarPathFinder:
    def __init__(self):
        self.utils = PathUtils()
        self.path = []
        self.steps = []
        self.finished = False
        self.start = None
        self.end = None

    def aStar(self, vertices, edges, s, r):

        g = WeightMatrix(vertices)  # function g(s->v)
        S = []  # OpenList S
        pi = {}  # Mapping pi: V -> V

        for v in vertices:
            pi[v] = None
            g[s, v] = inf
        g[s, s] = 0
        S.append(s)
        g[s, r] = self.utils.h(s, r)  # Precalculate h(s,r)
        selectedVertice = s  # First start with the starting vertice
        while len(S) != 0:
            minWeight = inf
            for vPrime in S:  # Find the vertice that minimizes g[s,vPrime]+ h(vPrime,r)
                if vPrime != s:
                    if (g[s, vPrime] + self.utils.h(vPrime, r)) < minWeight:
                        minWeight = g[s, vPrime] + self.utils.h(vPrime, r)
                        selectedVertice = vPrime

            # If the target vertice is reached, terminate
            if selectedVertice == r and g[selectedVertice, r] < inf:
                return pi

            if selectedVertice in S:  # S <- S \ {v}
                S.pop(S.index(selectedVertice))

            # For each successor of selectedVertice
            for u in self.utils.getSuccessors(selectedVertice, edges, vertices):
                if pi[u] is None:  # If it is NIL then open u
                    if not (u in S):  # S <- S U {u}
                        S.append(u)
                    g[s, u] = g[s, selectedVertice] + self.utils.manhattanDistance(selectedVertice, u)  # Update the weight
                    pi[u] = selectedVertice  # Update the mapping
                    g[u, r] = self.utils.h(u, r)  # Precalculate h(u,r)

                elif ((u in S) and ((g[s, selectedVertice] + self.utils.manhattanDistance(selectedVertice, u)) < g[
                    s, u])):  # g(s->v) + weight(v,u) < g(s->u) then open u
                    if not (u in S):  # S <- S U {u}
                        S.append(u)
                    g[s, u] = g[s, selectedVertice] + self.utils.manhattanDistance(selectedVertice, u)  # Update the weight
                    pi[u] = selectedVertice  # Update the mapping
                    g[u, r] = self.utils.h(u, r)  # Precalculate h(u,r)

    def findPath(self, vertices, map, start, end):
        result = self.aStar(vertices, map, start, end)
        self.steps, self.path, self.finished = self.utils.calculatePathFromMapping(result, start, end)

    def nextPointToMove(self):
        return self.path[1][1] if len(self.path) > 1 else self.path[0][1]

    def plotPath(self, fig, ax, vertices, map, walls, start, end, drawAllPoints=False, initialRun=False):

        if initialRun:
            self.start = start
            self.end = end

        if drawAllPoints:
            allVerticeX, allVerticeY = [], []
            for v in vertices:
                allVerticeX.append(v[0])
                allVerticeY.append(v[1])

            ax.scatter(allVerticeX, allVerticeY, color='hotpink')
            ax.axis('equal')  # Equal aspect ratio
            for e in map:
                ax.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], 'm')

        pathVerticeX, pathVerticeY = [], []
        for v in self.steps:
            pathVerticeX.append(v[0])
            pathVerticeY.append(v[1])

        ax.scatter(pathVerticeX, pathVerticeY, color='blue')
        ax.axis('equal')  # Equal aspect ratio

        for e in walls:
            ax.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], 'k', linewidth=10)

        if not self.finished:
            ax.plot(start[0], start[1], 'ko')
            ax.text(start[0], start[1], 'Agent', verticalalignment='bottom', horizontalalignment='right', color='blue')
            for e in self.path:
                ax.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], 'k')
        else:
            ax.plot(self.end[0], self.end[1], 'ko')
            ax.text(self.end[0], self.end[1], 'Agent', verticalalignment='bottom', horizontalalignment='right', color='blue')
            ax.text(self.end[0], self.end[1], f'Maze is completed',
                    horizontalalignment='center', verticalalignment='top',
                    fontsize=40, color='green')

        ax.plot(self.start[0], self.start[1], 'go')
        ax.text(self.start[0], self.start[1], 'Start', verticalalignment='bottom', horizontalalignment='right', color='green')
        ax.plot(self.end[0], self.end[1], 'ro')
        ax.text(self.end[0], self.end[1], 'End', verticalalignment='bottom', horizontalalignment='right', color='red')
        ax.axis('square')

        return fig, ax