# Dynamic Maze Generation with Time-Dependent Randomness and Pathfinding

## Description

In this project, `Prim's Maze` will be created in randomized fashion by using `Linear Congruential Generator (LCG)`
random number generation method. Within the maze, `A*` algorithm will be implemented to navigate the
user from the start to the end.

## Installation

### Step 1: Clone the repository

First, clone the repository to your local machine and enter to the directory:

```sh
git clone https://github.com/afiratbeydilli/MMI513-TermProject.git
```
```sh
cd MMI513-TermProject
```

### Step 2: Create a Virtual Environment (Optional)
It's a good practice to use a virtual environment to manage dependencies & prevent cyclic dependencies.
Even though it is not mandatory, it is strongly recommended to set up a virtual environment before
installing the necessary modules.

#### Using venv (Python 3.3+)

1) Create a virtual environment:

```sh
python3 -m venv venv
```
This creates a directory named venv which contains your virtual environment.

2) Activate the virtual environment:

On Windows:

```sh
venv\Scripts\activate
```

On macOS and Linux:

```sh
source venv/bin/activate
```

### Step 3: Install Dependencies
With the virtual environment activated, install the required dependencies using pip:

```sh
pip install -r requirements.txt
```

This will install all the packages listed in the requirements.txt file.

## Usage

The project consists of two sections: the modules file and the main script. The modules file
contain the function definitions which are defined based on the term project explanation. The
main script calls the functions within modules folder whenever necessary and will produce the output of the program.
The usage is very simple:

Enter the directory & run the main script:
```sh
cd MMI513-TermProject
```
```sh
python main.py
```

## Contributing & License

The project is prepared by two individuals for `MMI513 - Algorithms for Interactive Systems` course.
+  Ahmet Fırat Beydilli
+  İsmail Hakkı Armutcu