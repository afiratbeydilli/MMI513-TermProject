from modules import maze_generation, pathfinding_algorithm, time_dependent_randomness
from modules.time_dependent_randomness import lcgRandomGenerator
from modules.maze_generation import PrimsMazeGenerator
from modules.pathfinding_algorithm import pathUtils, AStarPathFinder
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def update():
    pass

def main():
    dim = 10
    mazeGen = PrimsMazeGenerator()
    mazeGen.initMaze(dim, dim)
    mazeGen.plotMaze()

    rng = lcgRandomGenerator()
    [start,end] = rng.sample(mazeGen.vertices,2)
    print(start)
    print(end)
    pathFinder = AStarPathFinder()
    pathFinder.findPath(mazeGen.vertices, mazeGen.map,start,end)
    pathFinder.plotPath(mazeGen.vertices,mazeGen.map,mazeGen.walls,start,end,True)






if __name__ == "__main__":
    main()
    print("Main function")



