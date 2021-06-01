# 37. Sudoku Solver (Hard)

'''
PRECONDITIONS: Sudoku board with the minimun number of seed values to solve the puzzle
POSCONDITIONS: solved Sudoku board (in-place)
BASIC STEPS: backtracking with pre-solving
* pre-solving uses a bit of additional processing and memory to determine the minimal number of candidate values for open cells
* which minimizes the search combinations during backtracking and significantly improves the performance of the overall algorithm
COMPLEXITY: time O(N!^9) where N is the max open cells in any sub-cube after all seeds have been determined; space O(81) cells
'''

def solveSudoku(board):
    """
    Do not return anything, modify board in-place instead.
    """
    BOARDSIZE = 9
    CUBESIZE = 3
    CUBEMAP = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    EMPTY = '.'
    ROW = 'row'
    COL = 'col'
    CANDIDATES = 'candidates'
    cubes = list()
    boardSolved = False

    # HELPERS
    def getBoardCoordinates(cube, cell):
        # returns the board coordinates (row, col) of a cell in a cube
        coordinates = CUBEMAP[cell]
        offsets = CUBEMAP[cube]
        return coordinates[0] + offsets[0] * CUBESIZE, coordinates[1] + offsets[1] * CUBESIZE

    def candidateValid(row, col, candidate):
        # returns true if candidate can be placed in the board at position (row, col) without conflicts
        # compare candidate to values in it's row
        for c in range(0, BOARDSIZE):
            if c != col and candidate == board[row][c]:
                return False
        # compare candidate to values in it's col
        for r in range(0, BOARDSIZE):
            if r != row and candidate == board[r][col]:
                return False
        return True

    def printCube(cube):
        # for debugging - displays a particular cube to standard output
        print()
        print('Cube:', cube)
        line = ''
        for cell in range(0, BOARDSIZE):
            r, c = getBoardCoordinates(cube, cell)
            if cell > 0 and cell % CUBESIZE == 0: line += '\n'
            line += board[r][c]
        print(line, '\n')

    def printBoard():
        # for debugging - displays the entire board on standard output seperated by individual cubes
        for row, values in enumerate(board):
            line = ''
            if row > 0 and row % CUBESIZE == 0:
                print()
            for col, val in enumerate(values):
                if col > 0 and col % CUBESIZE == 0:
                    line += ' '
                line += val if val != EMPTY else '_'
            print(line)
        print()

    def printCells():
        # for debugging - displays the candidate values for each open cell of the board to standard output
        for i, cube in enumerate(cubes):
            print('cube:', i)
            for i, cell in enumerate(cube):
                print(i, cell)
            print()

    # SETUP
    # generate the list of valid candidates for each open (non-seed) cell
    def initcubes():
        def cubeParms(cube):
            candidates = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            cells = []
            for cell in range(0, BOARDSIZE):
                row, col = getBoardCoordinates(cube, cell)
                val = board[row][col]
                if val == EMPTY:
                    cells.append({ROW: row, COL: col})
                else:
                    candidates.remove(val)
            return cells, candidates

        def cellParms(cube, cells, candidates):
            for cell in cells:
                row = cell[ROW]
                col = cell[COL]
                cellCandidates = list()
                for candidate in candidates:
                    if candidateValid(row, col, candidate):
                        # add candidate and it's availability status
                        cellCandidates.append(candidate)
                cell[CANDIDATES] = cellCandidates
            return cells

        # initcubes()
        for cube in range(0, BOARDSIZE):
            cells, candidates = cubeParms(cube)
            cubes.append(cellParms(cube, cells, candidates))

    # PRESOLVE
    # set cells to solve with a single candidate as seeds
    #   remove seeds in other cells
    #   repeat this process until all seeds have been discovered and their appearences in other cells removed
    def preSolve():
        def mineSeeds():
            # set calculated seeds
            seeds = list()

            def mineSeedsCube(cube):
                seedsAdded = False
                seeds.clear()

                # find default seeds
                for cell in cube:
                    if len(cell[CANDIDATES]) == 1:
                        val = cell[CANDIDATES][0]
                        board[cell[ROW]][cell[COL]] = val
                        seeds.append(val)
                        seedsAddedCnt = True

                # remove mined seeds from candidate lists of other cells
                for seed in seeds:
                    for cell in cube:
                        if seed in cell[CANDIDATES]:
                            cell[CANDIDATES].remove(seed)

                # remove empty candidate lists
                for cell in range(len(cube) - 1, -1, -1):
                    if len(cube[cell][CANDIDATES]) == 0:
                        cube.pop(cell)
                return seedsAdded

            # mineSeeds()
            seedsMinded = False
            for cube in cubes:
                seedsMinded = mineSeedsCube(cube) or seedsMinded
            return seedsMinded

        def mineCandidates():
            # remove candidates that were invalidated by the minded seeds
            minedCandidates = 0
            for cube in cubes:
                for cell in cube:
                    row, col = cell[ROW], cell[COL]
                    for i in range(len(cell[CANDIDATES]) - 1, -1, -1):
                        val = cell[CANDIDATES][i]
                        if not candidateValid(row, col, val):
                            cell[CANDIDATES].pop(i)
                            minedCandidates += 1
            return minedCandidates

        # preSolve()
        while True:
            seeds = mineSeeds()
            candidates = mineCandidates()
            if not seeds and not candidates:
                break

    # BACKTRACK
    def reject(cube, cell, candidate):
        # accommodate first pass
        if cube is None:
            return False

        # get candidate location
        row, col = cubes[cube][cell][ROW], cubes[cube][cell][COL]

        # reject if candidate is already deployed in row or col
        if not candidateValid(row, col, candidate):
            return True

        # deploy candidate to board
        board[row][col] = candidate
        return False

    def nextCell(cube, cell, explored):
        nonlocal boardSolved
        # return next cube, cell, and cell's first candidate
        # if no more cells to solve, return None, None, None

        # accomodate first pass
        if cube is None:
            cube = 0
            cell = -1

        # advanced to next cell of current cube
        cell += 1

        # if completed current cube, advance to next cube with cells to solve
        if cell == len(cubes[cube]):
            cube += 1
            while cube < BOARDSIZE and len(cubes[cube]) == 0:
                cube += 1

            # check for completed board
            if cube == BOARDSIZE:
                boardSolved = True
                return None, None, None

            # reset cell index to solve first cell of next cube
            cell = 0

        # return first candidate of new cell
        return cube, cell, nextCandidate(cube, cell, explored)

    def nextCandidate(cube, cell, explored):
        # return next candidate to solve of cube
        nonlocal boardSolved

        # accommodate first pass and cubes with no cells to solve
        if cube is None or len(cubes[cube]) == 0:
            return None

        # created set of candidates that have already been deployed to cube
        deployed = set()
        for c in range(0, cell):
            row, col = cubes[cube][c][ROW], cubes[cube][c][COL]
            deployed.add(board[row][col])

        # return first available candidate - that has not already been deployed or explored
        for val in cubes[cube][cell][CANDIDATES]:
            if val not in deployed and val not in explored:
                return val

        # no valid candidates - all have been deployed or already explored (and rejected)
        # remove deployed values in the cell to maintain the board's integrity while backtracking
        if not boardSolved:
            row, col = cubes[cube][cell][ROW], cubes[cube][cell][COL]
            board[row][col] = EMPTY
        return None

    def solve(cube, cell, candidate):
        explored = set()  # list of candidates that have already been evaluated for cell
        if reject(cube, cell, candidate): return
        cube, cell, candidate = nextCell(cube, cell, explored)
        while cube is not None and candidate is not None:
            solve(cube, cell, candidate)
            explored.add(candidate)
            candidate = nextCandidate(cube, cell, explored)

    # solveSudoku()
    # identiry open cells and their solution candidates
    initcubes()

    # show board and open cell candidates
    printBoard()
    printCells()

    # identify additional seeds (cells with a single candidate)
    # and remove those seeds from other candidate list
    # repeat these two steps until all possible seeds have been determined
    preSolve()

    # show board with deduced seeds and updated candidate lists
    printBoard()
    printCells()

    # use backtracking to deduce any remaining open cells
    solve(None, None, None)

    # show completed board
    printBoard()


# sudoku board to solve
board = [[".",".","9","7","4","8",".",".","."],
         ["7",".",".",".",".",".",".",".","."],
         [".","2",".","1",".","9",".",".","."],
         [".",".","7",".",".",".","2","4","."],
         [".","6","4",".","1",".","5","9","."],
         [".","9","8",".",".",".","3",".","."],
         [".",".",".","8",".","3",".","2","."],
         [".",".",".",".",".",".",".",".","6"],
         [".",".",".","2","7","5","9",".","."]]

solveSudoku(board)