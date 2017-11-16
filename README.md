# sudoku
A simple python script to generate a random sudoku and the method of solving.

## Introduction
Here I use the [Algorithm X](http://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html) to solve a sudoku.

The idea is to generate a full sudoku matrix and iteratively remove one random cell of it until it reaches its maximum iteration times or start to have multiple solutions. 

Here you can choose the difficulty of a sudoku by setting the maximum iteration times. 

## Usage
Type the following in the terminal and you will get a sudoku print out in the console. 

```bash
python3 generate_sudoku.py -n 81
```

Here you can choose any positive number to replace [81]


Hope you enjoy! Later I'll publish the sudoku using Django. 


