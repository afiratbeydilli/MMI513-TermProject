from modules.maze_generation import PrimsMazeGenerator
from modules.pathfinding_algorithm import AStarPathFinder
from modules.time_dependent_randomness import lcgRandomGenerator
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML
class DynamicMaze:
    def __init__(self):
        self.dim = 10
        self.mazeGen = PrimsMazeGenerator()
        self.rng = lcgRandomGenerator()
        self.pathFinder = AStarPathFinder()
        self.start = (0,0)
        self.end = (0,0)
        self.currentPos = (0,0)
        self.path = []
        self.fig = None
        self.ax = None


    def initializeStructures(self):
        self.fig,self.ax = plt.subplots(figsize=(15, 15))
        self.path.append(self.start)
        self.mazeGen.initMaze(self.dim, self.dim)
        [self.start, self.end] = self.rng.sample(self.mazeGen.vertices, 2)
        self.pathFinder.findPath(self.mazeGen.vertices, self.mazeGen.map, self.start, self.end)
        self.pathFinder.plotPath(self.fig,self.ax,self.mazeGen.vertices, self.mazeGen.map, self.mazeGen.walls, self.start, self.end, False)

        self.fig.savefig("foundPath.png")


    def updateMaze(self,frame):
        print(self.currentPos ,self.end)
        if(self.currentPos != self.end):
            print(frame)
            self.ax.clear()
            self.ax.set_title(f'Frame {frame}')
            self.currentPos = self.pathFinder.path[1][1]
            self.path.append(self.currentPos)
            self.mazeGen.initMaze(self.dim, self.dim)
            self.pathFinder.findPath(self.mazeGen.vertices, self.mazeGen.map, self.currentPos, self.end)
            self.fig, self.ax = self.pathFinder.plotPath(self.fig, self.ax, self.mazeGen.vertices, self.mazeGen.map, self.mazeGen.walls, self.currentPos, self.end, False)
            #self.fig.savefig("updatePath.png")

    def animate(self):
        ani = animation.FuncAnimation(self.fig,self.updateMaze,20,interval=1500)
        ani.save("path_animation.gif",writer='pillow')










