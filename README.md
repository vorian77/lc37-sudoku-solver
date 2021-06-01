# LeetCode.com Problem 37 - Sudoku Solver

This is an implementation of a Sudoku puzzle solver based on 
[LeetCode.com Problem #37](https://leetcode.com/problems/sudoku-solver/).

I completed this project to reinforce my understanding of the backtracking algorithm, 
which I was introduced to while solving [LeetCode.com Problem #51 N-Queens](https://leetcode.com/problems/n-queens/). 

Primary components:
* **initcubes()** - creates a list of legal candidates for all solve-cells.
  Solve-cells are the empty, non-seed cells of the puzzle.
  Seed-cells are cells that have been assigned their correct value. 
  All well-formed Sudoku puzzles begin with several seed-cells.
  

* **preSolve()** - identifies all solve-cells with a single candidate value and assigns that value to the cell,
  effectively making the cell a seed-cell. 
  Next it removes the newly created seed cell value from any candidate lists of solve-cells in its cube (3x3 area of puzzle).
  This reduces some candidate list to a single value. 
  It repeats these two steps until all possible seed cells have been identified, leaving the candidate lists for the 
  solve-cells as short as possible.
  The minimized candidate lists reduce the potential number of backtracking passes, which generally dramatically 
  improves the performance of the overall algorithm.
  

* **solve** - uses a backtracking algorithm to determine the correct value for each of the solve-cells in the puzzle.


(Helper) visual display functions:
* **printCells()** - displays to standard output the solve-cells and candidate values for each cube in the puzzle.


* **printBoard()** - displays to standard output the current state of the puzzle. 
  Unsolved cells of the puzzle are represented by *.
  
## Table of Contents

* [Instructions](#instructions)
* [Program Outputs](#outputs)
* [Support](#support)
* [Contributing](#contributing)
* [Authors and Acknowledgement](#authors-and-acknowledgement)

## Instructions

1. Copy the main.py file.
2. Update the "board" global variable with the configuration of your (well-formed) Sudoku puzzle.
3. Execute the program using Python 3 - `python3 main.py`.

## Outputs

### "board" variable used to define a cube to be solved.
```
board = [[".",".","9","7","4","8",".",".","."],
         ["7",".",".",".",".",".",".",".","."],
         [".","2",".","1",".","9",".",".","."],
         [".",".","7",".",".",".","2","4","."],
         [".","6","4",".","1",".","5","9","."],
         [".","9","8",".",".",".","3",".","."],
         [".",".",".","8",".","3",".","2","."],
         [".",".",".",".",".",".",".",".","6"],
         [".",".",".","2","7","5","9",".","."]]
```

### "printBoard()" output of unsolved puzzle.
```
**9 748 ***
7** *** ***
*2* 1*9 ***

**7 *** 24*
*64 *1* 59*
*98 *** 3**

*** 8*3 *2*
*** *** **6
*** 275 9**
```

### "printCells()" output of cell candidates before preSolve has been executed.
```
cube: 0
0 {'row': 0, 'col': 0, 'candidates': ['1', '3', '5', '6']}
1 {'row': 0, 'col': 1, 'candidates': ['1', '3', '5']}
2 {'row': 1, 'col': 1, 'candidates': ['1', '3', '4', '5', '8']}
3 {'row': 1, 'col': 2, 'candidates': ['1', '3', '5', '6']}
4 {'row': 2, 'col': 0, 'candidates': ['3', '4', '5', '6', '8']}
5 {'row': 2, 'col': 2, 'candidates': ['3', '5', '6']}

cube: 1
0 {'row': 1, 'col': 3, 'candidates': ['3', '5', '6']}
1 {'row': 1, 'col': 4, 'candidates': ['2', '3', '5', '6']}
2 {'row': 1, 'col': 5, 'candidates': ['2', '6']}
3 {'row': 2, 'col': 4, 'candidates': ['3', '5', '6']}

cube: 2
0 {'row': 0, 'col': 6, 'candidates': ['1', '6']}
1 {'row': 0, 'col': 7, 'candidates': ['1', '3', '5', '6']}
2 {'row': 0, 'col': 8, 'candidates': ['1', '2', '3', '5']}
3 {'row': 1, 'col': 6, 'candidates': ['1', '4', '6', '8']}
4 {'row': 1, 'col': 7, 'candidates': ['1', '3', '5', '6', '8']}
5 {'row': 1, 'col': 8, 'candidates': ['1', '2', '3', '4', '5', '8', '9']}
6 {'row': 2, 'col': 6, 'candidates': ['4', '6', '7', '8']}
7 {'row': 2, 'col': 7, 'candidates': ['3', '5', '6', '7', '8']}
8 {'row': 2, 'col': 8, 'candidates': ['3', '4', '5', '7', '8']}

cube: 3
0 {'row': 3, 'col': 0, 'candidates': ['1', '3', '5']}
1 {'row': 3, 'col': 1, 'candidates': ['1', '3', '5']}
2 {'row': 4, 'col': 0, 'candidates': ['2', '3']}
3 {'row': 5, 'col': 0, 'candidates': ['1', '2', '5']}

cube: 4
0 {'row': 3, 'col': 3, 'candidates': ['3', '5', '6', '9']}
1 {'row': 3, 'col': 4, 'candidates': ['3', '5', '6', '8', '9']}
2 {'row': 3, 'col': 5, 'candidates': ['6']}
3 {'row': 4, 'col': 3, 'candidates': ['3']}
4 {'row': 4, 'col': 5, 'candidates': ['2', '7']}
5 {'row': 5, 'col': 3, 'candidates': ['4', '5', '6']}
6 {'row': 5, 'col': 4, 'candidates': ['2', '5', '6']}
7 {'row': 5, 'col': 5, 'candidates': ['2', '4', '6', '7']}

cube: 5
0 {'row': 3, 'col': 8, 'candidates': ['1', '8']}
1 {'row': 4, 'col': 8, 'candidates': ['7', '8']}
2 {'row': 5, 'col': 7, 'candidates': ['1', '6', '7']}
3 {'row': 5, 'col': 8, 'candidates': ['1', '7']}

cube: 6
0 {'row': 6, 'col': 0, 'candidates': ['1', '4', '5', '6', '9']}
1 {'row': 6, 'col': 1, 'candidates': ['1', '4', '5', '7']}
2 {'row': 6, 'col': 2, 'candidates': ['1', '5', '6']}
3 {'row': 7, 'col': 0, 'candidates': ['1', '2', '3', '4', '5', '8', '9']}
4 {'row': 7, 'col': 1, 'candidates': ['1', '3', '4', '5', '7', '8']}
5 {'row': 7, 'col': 2, 'candidates': ['1', '2', '3', '5']}
6 {'row': 8, 'col': 0, 'candidates': ['1', '3', '4', '6', '8']}
7 {'row': 8, 'col': 1, 'candidates': ['1', '3', '4', '8']}
8 {'row': 8, 'col': 2, 'candidates': ['1', '3', '6']}

cube: 7
0 {'row': 6, 'col': 4, 'candidates': ['6', '9']}
1 {'row': 7, 'col': 3, 'candidates': ['4', '9']}
2 {'row': 7, 'col': 4, 'candidates': ['9']}
3 {'row': 7, 'col': 5, 'candidates': ['1', '4']}

cube: 8
0 {'row': 6, 'col': 6, 'candidates': ['1', '4', '7']}
1 {'row': 6, 'col': 8, 'candidates': ['1', '4', '5', '7']}
2 {'row': 7, 'col': 6, 'candidates': ['1', '4', '7', '8']}
3 {'row': 7, 'col': 7, 'candidates': ['1', '3', '5', '7', '8']}
4 {'row': 8, 'col': 7, 'candidates': ['1', '3', '8']}
5 {'row': 8, 'col': 8, 'candidates': ['1', '3', '4', '8']}
```

### "printBoard()" output of puzzle after preSolve() has been executed and additional seed-cells identified.
```
**9 748 ***
7** 6*2 ***
*2* 1*9 ***

**7 986 241
264 317 598
198 524 367

*** 863 *2*
*** 491 **6
*** 275 9**
```


### "printCells()" output of cell candidates after preSolve has been executed.
```
cube: 0
0 {'row': 0, 'col': 0, 'candidates': ['3', '5', '6']}
1 {'row': 0, 'col': 1, 'candidates': ['1', '3', '5']}
2 {'row': 1, 'col': 1, 'candidates': ['1', '3', '4', '5', '8']}
3 {'row': 1, 'col': 2, 'candidates': ['1', '3', '5']}
4 {'row': 2, 'col': 0, 'candidates': ['3', '4', '5', '6', '8']}
5 {'row': 2, 'col': 2, 'candidates': ['3', '5', '6']}

cube: 1
0 {'row': 1, 'col': 4, 'candidates': ['3', '5']}
1 {'row': 2, 'col': 4, 'candidates': ['3', '5']}

cube: 2
0 {'row': 0, 'col': 6, 'candidates': ['1', '6']}
1 {'row': 0, 'col': 7, 'candidates': ['1', '3', '5']}
2 {'row': 0, 'col': 8, 'candidates': ['2', '3', '5']}
3 {'row': 1, 'col': 6, 'candidates': ['1', '4', '8']}
4 {'row': 1, 'col': 7, 'candidates': ['1', '3', '5', '8']}
5 {'row': 1, 'col': 8, 'candidates': ['3', '4', '5', '9']}
6 {'row': 2, 'col': 6, 'candidates': ['4', '6', '7', '8']}
7 {'row': 2, 'col': 7, 'candidates': ['3', '5', '7', '8']}
8 {'row': 2, 'col': 8, 'candidates': ['3', '4', '5']}

cube: 3
0 {'row': 3, 'col': 0, 'candidates': ['3', '5']}
1 {'row': 3, 'col': 1, 'candidates': ['3', '5']}

cube: 4

cube: 5

cube: 6
0 {'row': 6, 'col': 0, 'candidates': ['4', '5', '9']}
1 {'row': 6, 'col': 1, 'candidates': ['1', '4', '5', '7']}
2 {'row': 6, 'col': 2, 'candidates': ['1', '5']}
3 {'row': 7, 'col': 0, 'candidates': ['3', '5', '8']}
4 {'row': 7, 'col': 1, 'candidates': ['3', '5', '7', '8']}
5 {'row': 7, 'col': 2, 'candidates': ['2', '3', '5']}
6 {'row': 8, 'col': 0, 'candidates': ['3', '4', '6', '8']}
7 {'row': 8, 'col': 1, 'candidates': ['1', '3', '4', '8']}
8 {'row': 8, 'col': 2, 'candidates': ['1', '3', '6']}

cube: 7

cube: 8
0 {'row': 6, 'col': 6, 'candidates': ['1', '4', '7']}
1 {'row': 6, 'col': 8, 'candidates': ['4', '5']}
2 {'row': 7, 'col': 6, 'candidates': ['7', '8']}
3 {'row': 7, 'col': 7, 'candidates': ['3', '5', '7', '8']}
4 {'row': 8, 'col': 7, 'candidates': ['1', '3', '8']}
5 {'row': 8, 'col': 8, 'candidates': ['3', '4']}
```

### "printBoard()" output of solved puzzle.
```
519 748 632
783 652 419
426 139 875

357 986 241
264 317 598
198 524 367

975 863 124
832 491 756
641 275 983
```

## Support

Please open an issue to receive help. 

## Contributing

Pull requests are welcome. Please open an issue to discuss any changes you would like to make or see.

## Authors and Acknowledgement

This project originated as a solution to [LeetCode.com problem 37](https://leetcode.com/problems/sudoku-solver/).

