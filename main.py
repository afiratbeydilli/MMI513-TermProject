from modules import maze_generation, pathfinding_algorithm, time_dependent_randomness
from modules.time_dependent_randomness import lcgRandomGenerator
from modules.maze_generation import PrimsMazeGenerator
from modules.pathfinding_algorithm import pathUtils, AStarPathFinder
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML

def update():
    pass

def main():
    dim = 10
    mazeGen = PrimsMazeGenerator()
    mazeGen.initMaze(dim, dim)
    mazeGen.plotMaze()

    pathFinder = AStarPathFinder()
    pathFinder.findPath(mazeGen.vertices, mazeGen.map,(0,0),(9,4))
    pathFinder.plotPath(mazeGen.vertices,mazeGen.map,mazeGen.walls,(0,0),(9,4),True)




if __name__ == "__main__":
    main()
    print("Main function")



