import numpy as np
import matplotlib.pyplot as plt
def maze_generation():
    print("maze_generation algorithm")

class undirectedGraph:
    def __init__(self):
        super().__init__()
    def getGraph(self, xnum=30, ynum=30):
        G = {'V': [], 'E': []}  # We will use a dictionary for simplicity
        for xind in range(xnum):
            for yind in range(ynum):
                G['V'].append((xind, yind))

        # Traverse north first
        for pt in G['V']:
            vtn = self.north(pt[0], pt[1])
            if self.isvertex(vtn, G['V']):
                G['E'].append((pt, vtn))

        # Traverse east second
        for pt in G['V']:
            vte = self.east(pt[0], pt[1])
            if self.isvertex(vte, G['V']):
                G['E'].append((pt, vte))
        return G

    def north(self, xind, yind):
        node = (xind, yind + 1)
        return node

    def south(self, xind, yind):
        node = (xind, yind - 1)
        return node

    def east(self, xind, yind):
        node = (xind + 1, yind)
        return node

    def west(self, xind, yind):
        node = (xind - 1, yind)
        return node

    def isvertex(self, node, vertices):
        return node in vertices



    def randomnode(self, vertices):
        vertices = list(vertices)
        randind = np.random.randint(0, len(vertices))
        return vertices[randind]

class primsMazeGenerator:
    def __init__(self):
        super().__init__()

    def inSet(self, element, Set):  # Determine if the given element is in the given set
        for s in Set:  # Returns true if found
            if (element == s):
                return True
        return False

    def endIntersect(self, set1, set2):  # Determine if two given ends intersects
        count = 0
        for s1 in set1:
            for s2 in set2:
                if (s1 == s2):
                    count += 1
        return count

    def intersectionSize(self, l, C):  # Determine the intersection length
        count = 0
        if (self.inSet(l[0], C)):
            count += 1
        if (self.inSet(l[1], C)):
            count += 1
        return count

    def getpPrimmsMaze(self, xnum=30, ynum=30):
        assert (type(xnum) == int and type(ynum) == int)  # Assertions
        assert (xnum > 0 and ynum > 0)  # Both inputs must be positive integers
        graphGenerator = undirectedGraph()
        G = graphGenerator.getGraph(xnum, ynum)  # Construct the undirected connection graph with the given parameters
        W = set(G['E'].copy())  # Initialize walls
        V = set(G['V'].copy())  # Initialize edges

        L = set()  # Set of walls to check out, initally empty
        C = set()  # Visited Cells, initally empty
        c = graphGenerator.randomnode(V)  # select c in V randomly

        for w in W:  # Initalize L with the neighbors of c
            if (self.inSet(c, w)):
                L.add(w)

        while len(L):
            l = graphGenerator.randomnode(L)  # Select l in L randomly
            if self.intersectionSize(l, C) <= 1:  # |ends(l) n C| <=1
                C.add(l[0])  # C <- C u ends(l)
                C.add(l[1])
                W.remove(l)  # Remove the wall
                for w in W:
                    if self.endIntersect(l, w):
                        if self.inSet(w, L) != True:
                            L.add(w)  # Add the neighbouring walls
            L.remove(l)

        P = {'V': G['V'].copy(), 'E': list(W)}
        return P
    def plotgraph(self, G, vertexflag=False):
        plt.rcParams['figure.figsize'] = [15, 15]
        plt.figure()
        for e in G['E']:
            vec = np.array([e[1][0] - e[0][0], e[1][1] - e[0][1]])
            ort = np.array([-vec[1], vec[0]])
            olen = np.linalg.norm(ort)
            ort = ort / olen
            sum = np.array([(e[1][0] + e[0][0]) / 2, (e[1][1] + e[0][1]) / 2])
            startp = sum - ort / 2
            endp = sum + ort / 2
            plt.plot((startp[0], endp[0]), (startp[1], endp[1]), 'k', linewidth=10)
            if vertexflag:
                for v in G['V']:
                    plt.plot(float(v[0]), float(v[1]), 'ro')

        plt.axis('square')
        plt.savefig("primsMaze.png")
        plt.close()  # Close the figure to release memory
