from modules import maze_generation, pathfinding_algorithm, time_dependent_randomness
from modules.time_dependent_randomness import lcgRandomGenerator
from modules.maze_generation import PrimsMazeGenerator
from modules.pathfinding_algorithm import pathUtils, AStarPathFinder
from modules.dynamic_maze import DynamicMaze
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def update():
    pass

def main():
    dynamicMaze = DynamicMaze()
    dynamicMaze.initializeStructures()
    #dynamicMaze.updateMaze(2)
    dynamicMaze.animate()








if __name__ == "__main__":
    main()
    print("Main function")



