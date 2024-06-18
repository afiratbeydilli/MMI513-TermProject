from modules import DynamicMaze
from modules.dynamic_maze import MAX_NUM_OF_FRAMES

def update():
    pass

def main():
    dynamicMaze = DynamicMaze()
    dynamicMaze.animate(MAX_NUM_OF_FRAMES)
    if dynamicMaze.pathFinder.finished:
        print("Maze is successfully solved")


if __name__ == "__main__":
    main()



