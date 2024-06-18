from .maze_generation import PrimsMazeGenerator
from .pathfinding_algorithm import AStarPathFinder
from .time_dependent_randomness import LCGRandomGenerator
import matplotlib.pyplot as plt
import matplotlib.animation as animation

MAX_NUM_OF_FRAMES = 20
class DynamicMaze:
    def __init__(self, dim=6):
        self.dim = dim
        self.mazeGen = PrimsMazeGenerator()
        self.rng = LCGRandomGenerator()
        self.pathFinder = AStarPathFinder()
        self.start = (0, 0)
        self.end = (0, 0)
        self.currentPos = (0, 0)
        self.path = []
        self.fig = None
        self.ax = None

    def initializeStructures(self):
        self.ax.clear()
        self.path.append(self.start)
        self.mazeGen.initMaze(self.dim, self.dim)
        [self.start, self.end] = self.rng.sample(self.mazeGen.vertices, 2)
        self.pathFinder.findPath(self.mazeGen.vertices, self.mazeGen.map, self.start, self.end)
        self.fig, self.ax = self.pathFinder.plotPath(self.fig, self.ax, self.mazeGen.vertices,
                                                     self.mazeGen.map, self.mazeGen.walls,
                                                     self.start, self.end,
                                                     False, True)

        self.fig.savefig("foundPath.png")

    def updateMaze(self, frame):

        if frame == 0:
            self.initializeStructures()
            self.ax.set_title(f'Frame {frame}')

        else:
            if not self.pathFinder.finished:
                self.ax.clear()
                self.ax.set_title(f'Frame {frame}')
                self.currentPos = self.pathFinder.nextPointToMove()
                self.path.append(self.currentPos)
                self.mazeGen.initMaze(self.dim, self.dim)
                self.pathFinder.findPath(self.mazeGen.vertices, self.mazeGen.map, self.currentPos, self.end)
                self.fig, self.ax = self.pathFinder.plotPath(self.fig, self.ax, self.mazeGen.vertices,
                                                             self.mazeGen.map, self.mazeGen.walls,
                                                             self.currentPos, self.end,
                                                             False, False)

            if not self.pathFinder.finished and frame == (MAX_NUM_OF_FRAMES - 1):
                self.uncompletedMaze()

        self.ax.set_xlim(-1, self.dim)
        self.ax.set_ylim(-1, self.dim)
        return self.fig, self.ax

    def uncompletedMaze(self):
        print(f"Unable to complete the maze in {MAX_NUM_OF_FRAMES} frames")
        self.ax.text(self.dim/2, self.dim/2, f'Unable to complete the maze in {MAX_NUM_OF_FRAMES} frames',
                      horizontalalignment='center', verticalalignment='center',
                      fontsize=40, color='red')
        self.ax.set_axis_off()

    def animate(self, frames=MAX_NUM_OF_FRAMES):
        self.fig, self.ax = plt.subplots(figsize=(15, 15))
        ani = animation.FuncAnimation(self.fig, self.updateMaze, frames, interval=1500)
        ani.save("path_animation.gif", writer='pillow')
