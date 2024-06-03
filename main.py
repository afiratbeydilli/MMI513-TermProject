from modules import maze_generation, pathfinding_algorithm, time_dependent_randomness
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
    anim = animation.FuncAnimation(fig, update, frames=30, interval=300)  # Check whether animation is imported
    # HTML(anim.to_html5_video())  # Check whether HTML is imported


if __name__ == "__main__":
    main()
    print("Main function")



