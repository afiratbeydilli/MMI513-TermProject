import matplotlib.pyplot as plt
inf = float('inf')
def pathfinding_algorithm():
    print("pathfinding_algorithm")


class pathUtils:
    def __init__(self):
        super().__init__()


    def plotPath(self,vertices, edges, start, end):  ## Plots the calculated path from the start and end vertices
        x, y = [], []
        for v in vertices:
            x.append(v[0])
            y.append(v[1])
            plt.scatter(x,y)
            plt.axis('equal')  # Equal aspect ratio
        for e in edges:
            plt.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], 'k')
            plt.text(start[0], start[1], 'Start', verticalalignment='bottom', horizontalalignment='right', color='blue')
            plt.text(end[0], end[1], 'End', verticalalignment='bottom', horizontalalignment='right', color='blue')
            ## Specify start and end vertices

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
            if (e[0] == selectedVertice and e[1] in vertices):
                if (not (e[1] in successorList)):
                    successorList.append(e[1])
            elif (e[1] == selectedVertice and e[0] in vertices):
                if (not (e[0] in successorList)):
                    successorList.append(e[0])
        return successorList

    def calculatePathFromMapping(self, res, s, r):  ## Calculate the path from the result of A* or Dijkstra Algorithm
        prev = res[r]
        steps = []
        steps.append(r)
        steps.append(prev)
        while (prev != s):
            prev = res[prev]
            steps.append(prev)

        travelledEdges = []
        for i in range(len(steps) - 1):
            travelledEdges.append(((steps[i]), (steps[i + 1])))
        travelledEdges.reverse()
        steps.reverse()
        return steps, travelledEdges


## A matrix class to store the distance between vertices this class implements g(s->r) function in A-Star and distance function in Dijkstra
class weightMatrix:
    def __init__(self,vertices):
        super().__init__()
        self.vertices = vertices
        self.matrix = []
        for i in range(len(vertices)):
            self.matrix.append([inf]*len(vertices))
    def __getitem__(self, index):
        s,v = index
        return self.matrix[self.vertices.index(s)][self.vertices.index(v)]
    def __setitem__(self, index, value):
        s,v = index
        self.matrix[self.vertices.index(s)][self.vertices.index(v)] = value

class AStarPathFinder:
    def __init__(self):
        super().__init__()
        self.utils = pathUtils()
        self.path = []
        self.steps = []

    def aStar(self,vertices, edges, s, r):

        g = weightMatrix(vertices)  # function g(s->v)
        S = []  # OpenList S
        pi = {}  # Mapping pi: V -> V
        for v in vertices:
            pi[v] = None
            g[s, v] = inf
        g[s, s] = 0
        S.append(s)
        g[s, r] = self.utils.h(s, r)  ## Precalculate h(s,r)
        selectedVertice = s  ##First start with the starting vertice
        while len(S) != 0:
            minWeight = inf
            for vPrime in S:  ##Find the vertice that minimizes g[s,vPrime]+ h(vPrime,r)
                if (vPrime != s):
                    if ((g[s, vPrime] + self.utils.h(vPrime, r)) < minWeight):
                        minWeight = g[s, vPrime] + self.utils.h(vPrime, r)
                        selectedVertice = vPrime

            if (selectedVertice == r and g[selectedVertice, r] < inf):  ## If the target vertice is reached, terminate
                return pi

            if (selectedVertice in S):  ## S <- S \ {v}
                S.pop(S.index(selectedVertice))

            for u in self.utils.getSuccessors(selectedVertice, edges, vertices):  ## For each successor of selectedVertice
                if (pi[u] == None):  ## If it is NIL then open u
                    if (not (u in S)):  ## S <- S U {u}
                        S.append(u)
                    g[s, u] = g[s, selectedVertice] + self.utils.manhattanDistance(selectedVertice, u)  ## Update the weight
                    pi[u] = selectedVertice  ##Update the mapping
                    g[u, r] = self.utils.h(u, r)  ##Precalculate h(u,r)

                elif ((u in S) and ((g[s, selectedVertice] + self.utils.manhattanDistance(selectedVertice, u)) < g[
                    s, u])):  ## g(s->v) + weight(v,u) < g(s->u) then open u
                    if (not (u in S)):  ## S <- S U {u}
                        S.append(u)
                    g[s, u] = g[s, selectedVertice] + self.utils.manhattanDistance(selectedVertice, u)  ## Update the weight
                    pi[u] = selectedVertice  ##Update the mapping
                    g[u, r] = self.utils.h(u, r)  ##Precalculate h(u,r)

    def findPath(self,vertices, map, start, end):
        result = self.aStar(vertices, map, start, end)
        self.steps, self.path = self.utils.calculatePathFromMapping(result, start, end)

    def plotPath(self, vertices, map, walls, start, end, tumNoktalarCizilsinMi = False):
        plt.rcParams['figure.figsize'] = [15, 15]
        plt.figure()
        if(tumNoktalarCizilsinMi):
            allVerticeX, allVerticeY = [], []
            for v in vertices:
                allVerticeX.append(v[0])
                allVerticeY.append(v[1])

            plt.scatter(allVerticeX, allVerticeY, color = 'hotpink')
            plt.axis('equal')  # Equal aspect ratio

        pathVerticeX,pathVerticeY = [],[]
        for v in self.steps:
            pathVerticeX.append(v[0])
            pathVerticeY.append(v[1])

        plt.scatter(pathVerticeX, pathVerticeY, color = 'blue')
        plt.axis('equal')  # Equal aspect ratio


        for e in map:
            plt.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], 'm')

        for e in walls:
            plt.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], 'k', linewidth=10)

        for e in self.path:
            plt.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], 'k')
            plt.text(start[0], start[1], 'Start', verticalalignment='bottom', horizontalalignment='right', color='blue')
            plt.text(end[0], end[1], 'End', verticalalignment='bottom', horizontalalignment='right', color='blue')

        plt.axis('square')
        plt.savefig("foundPath.png")
        plt.close()  # Close the figure to release memory
