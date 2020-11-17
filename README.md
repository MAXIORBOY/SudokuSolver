# Sudoku Solver is a program used for solving any (classic) Sudoku grid.
## Idea:
1. Find and fill an empty field with only one possibility.  
2. If there are no such fields, find an empty field with the lowest number of possibilities and fill it with a random (possible) option. 
3. Go back to the step 1.  

If at any time (after making an assumption) there is an empty field without any possibility, rollback the grid to the previous assumption, and make another one.  

## Launch:
Rewrite numbers from a grid into the sudoku.txt file and launch the program. An empty field is being represented by zero. Do not use comma, space or any other separators. You can find a valid example in the ```sudoku.txt``` file.
* Launch the ```RUN.py``` script.
* An executable (.exe) version is available in the ```Release``` folder.

## Technology: 
* ```Python``` 3.8
* ```matplotlib``` 3.3.2

## Screenshot:  
![SudokuSolver screenshot](https://user-images.githubusercontent.com/71539614/99324225-16df9180-2874-11eb-8815-6f0c9a3f7bdd.png)
