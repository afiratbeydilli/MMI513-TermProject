import numpy as np
import matplotlib.pyplot as plt
from shapely import Polygon, LineString
from shapely.ops import triangulate
import random
def pathfinding_algorithm():
    print("pathfinding_algorithm")

class pathUtils:
    def __init__(self):
        super().__init__()

    def plotpoly(self, poly, flag=True):  ## Plots a polynomial
        fig, ax = plt.subplots()
        if flag:
            ax.plot(poly[:, 1], poly[:, 0], 'o-r', linewidth=2)
        else:
            ax.plot(poly[:, 0], poly[:, 1], 'o-r', linewidth=2)
            ax.plot([poly[-1, 0], poly[0, 0]], [poly[-1, 1], poly[0, 1]], 'o-r', linewidth=2)
        return ax

    # Triangulation is carried out in the convex hull and not within the polygon.
    # We will select triangles within the polygon
    def triangulate_within(self, polygon):
        return [triangle for triangle in triangulate(polygon) if triangle.within(polygon)]

    def getgraph(self, points):  # We are not doing any type-checking, which is not good!
        polygon = Polygon(points)
        trig = self.triangulate_within(polygon)
        vertices = []
        edges = []
        for ply in trig:
            neighs = ply.intersection(trig)
            cp1 = ply.centroid
            vertices.append(cp1)
            ln = len(neighs)
            for ind in range(ln):
                neig = neighs[ind]
                # Two triangles are neighbours only when their intersection is a LineString
                if type(neig) == LineString:
                    cp2 = trig[ind].centroid
                    edges.append(LineString(
                        [cp1, cp2]))  # We are adding all edges twice so we will have to eliminate them at the end
        # Eliminate the duplicates now
        edgeiter = edges.copy()
        for edge in edgeiter:
            if len(np.where(edge.equals(edges) == True)[0]) > 1:
                edges.remove(edge)
        return vertices, edges

    def convertGraph(self, vertices, edges):  # Converts the vertices and edges returned from getGraph to be suitable for A* and Dijkstra algorithms
        v = []
        for vertice in vertices:
            v.append((round(vertice.x, 2), round(vertice.y, 2)))
        e = []
        for edge in edges:
            p1x = round(edge.coords[0][0], 2)
            p1y = round(edge.coords[0][1], 2)
            p2x = round(edge.coords[1][0], 2)
            p2y = round(edge.coords[1][1], 2)
            e.append(((p1x, p1y), (p2x, p2y)))
        return v, e

    def plotgraph(self, vertices, edges):  ## Plots the graph with edge weights in manhattan weight
        x, y = [], []
        for v in vertices:
            x.append(v[0])
            y.append(v[1])

        plt.scatter(np.array(x), np.array(y))
        plt.axis('equal')  # Equal aspect ratio
        for e in edges:
            plt.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], 'm')
            x = (e[0][0] + e[1][0]) / 2
            y = (e[0][1] + e[1][1]) / 2
            plt.text(x, y, f'{round(abs(e[0][0] - e[1][0]) + abs(e[0][1] - e[1][1]), 2)}', verticalalignment='bottom',
                     horizontalalignment='right', color='magenta')  # Text annotation
            ## Weight of an edge in manhattan metric

    def plotPath(self,vertices, edges, start, end):  ## Plots the calculated path from the start and end vertices
        x, y = [], []
        for v in vertices:
            x.append(v[0])
            y.append(v[1])
            plt.scatter(np.array(x), np.array(y))
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
        return steps, travelledEdges
    def plotSimpleRoom(self, aStarImplementor, simproom):
        vertices, edges = self.getgraph(simproom)
        vertices, edges = self.convertGraph(vertices, edges)

        s, r = random.sample(vertices, 2)
        res = aStarImplementor.aStar(vertices, edges, s, r)
        steps, travelledEdges = self.calculatePathFromMapping(res, s, r)
        plt.figure()
        self.plotpoly(simproom, False)
        self.plotgraph(vertices, edges)
        self.plotPath(steps, travelledEdges, s, r)
        plt.title('A* Algorithm on Simple Room')
        plt.savefig("aStar.png")
        plt.close()


## A matrix class to store the distance between vertices this class implements g(s->r) function in A-Star and distance function in Dijkstra
class weightMatrix:
    def __init__(self,vertices):
        super().__init__()
        self.vertices = vertices
        self.matrix = []
        for i in range(len(vertices)):
            self.matrix.append([np.inf]*len(vertices))
    def __getitem__(self, index):
        s,v = index
        return self.matrix[self.vertices.index(s)][self.vertices.index(v)]
    def __setitem__(self, index, value):
        s,v = index
        self.matrix[self.vertices.index(s)][self.vertices.index(v)] = value

class aStarImplementor:
    def __init__(self):
        super().__init__()

    def aStar(self,vertices, edges, s, r):
        util = pathUtils()
        g = weightMatrix(vertices)  # function g(s->v)
        S = []  # OpenList S
        pi = {}  # Mapping pi: V -> V
        for v in vertices:
            pi[v] = None
            g[s, v] = np.inf
        g[s, s] = 0
        S.append(s)
        g[s, r] = util.h(s, r)  ## Precalculate h(s,r)
        selectedVertice = s  ##First start with the starting vertice
        while len(S) != 0:
            minWeight = np.inf
            for vPrime in S:  ##Find the vertice that minimizes g[s,vPrime]+ h(vPrime,r)
                if (vPrime != s):
                    if ((g[s, vPrime] + util.h(vPrime, r)) < minWeight):
                        minWeight = g[s, vPrime] + util.h(vPrime, r)
                        selectedVertice = vPrime

            if (selectedVertice == r and g[selectedVertice, r] < np.inf):  ## If the target vertice is reached, terminate
                return pi

            if (selectedVertice in S):  ## S <- S \ {v}
                S.pop(S.index(selectedVertice))

            for u in util.getSuccessors(selectedVertice, edges, vertices):  ## For each successor of selectedVertice
                if (pi[u] == None):  ## If it is NIL then open u
                    if (not (u in S)):  ## S <- S U {u}
                        S.append(u)
                    g[s, u] = g[s, selectedVertice] + util.manhattanDistance(selectedVertice, u)  ## Update the weight
                    pi[u] = selectedVertice  ##Update the mapping
                    g[u, r] = util.h(u, r)  ##Precalculate h(u,r)

                elif ((u in S) and ((g[s, selectedVertice] + util.manhattanDistance(selectedVertice, u)) < g[
                    s, u])):  ## g(s->v) + weight(v,u) < g(s->u) then open u
                    if (not (u in S)):  ## S <- S U {u}
                        S.append(u)
                    g[s, u] = g[s, selectedVertice] + util.manhattanDistance(selectedVertice, u)  ## Update the weight
                    pi[u] = selectedVertice  ##Update the mapping
                    g[u, r] = util.h(u, r)  ##Precalculate h(u,r)