from modules import maze_generation, pathfinding_algorithm, time_dependent_randomness
from modules.time_dependent_randomness import lcgRandomGenerator
from modules.maze_generation import primsMazeGenerator
from modules.pathfinding_algorithm import pathUtils, aStarImplementor
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML

def update():
    pass

def main():
    maze_generation()
    pathfinding_algorithm()
    time_dependent_randomness()
    np.random.randint(5)  # Check whether numpy is imported
    fig = plt.figure()  # Check whether pyplot is imported
    #anim = animation.FuncAnimation(fig, update, frames=30, interval=300)  # Check whether animation is imported
    # HTML(anim.to_html5_video())  # Check whether HTML is imported
    prng = lcgRandomGenerator()
    print("Linear Congruential Method Random Numbers:")
    prng.spectraltest() ## perform the spectral test and save it to spectral_test.png
    rlist = prng.lcgrandom(num=100)
    print(rlist)

###############################################################
    print("Maze is generated in \"primmsMaze.png\"")
    mazeGen = primsMazeGenerator()
    P = mazeGen.getpPrimmsMaze(10,10)
    mazeGen.plotgraph(P)

#################################################################
    print("Simple A Star path finding is generated in \"aStar.png\"")
    simproom = np.array(
        [[0, 0], [3, 0], [3, 2], [4, 2], [4, 0], [5, 0], [5, 2], [7, 2], [7, 0], [12, 0], [12, 7], [7, 7], [7, 5],
         [3, 5], [3, 7], [0, 7]])
    pathFinderUtils = pathUtils()
    aStar = aStarImplementor()
    pathFinderUtils.plotSimpleRoom(aStar,simproom)


if __name__ == "__main__":
    main()
    print("Main function")



