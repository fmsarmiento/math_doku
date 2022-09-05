# Sudoku Time!
from concurrent.futures import thread
import random
from time import perf_counter
import copy
import threading

def generateInitialGridMatrix():
    '''Generates initial matrix for random sudoku generation.'''
    init_grid = []
    for i in range(0,3):
        out = []
        grid_init = list(range(1,10))
        for x in range(0,9):
            choice = random.choice(grid_init)
            grid_init.remove(choice)
            out.append(choice)
        init_grid.append([out[0:3],out[3:6],out[6:9]])
    out = []
    for idx, i in enumerate(init_grid):
        for row in i:
            if idx == 0: out.append(row + [0,0,0,0,0,0])
            elif idx == 1: out.append([0,0,0] + row + [0,0,0])
            else: out.append([0,0,0,0,0,0] + row)
    return out

def sudokuSolver(board, max_iterations):
    '''Solves the sudoku board.'''
    initial_board = copy.deepcopy(board)
    x = 0
    idx_row = 0
    grid = [[[],[],[]],[[],[],[]],[[],[],[]]]
    num_iters = 1
    while idx_row < len(board):
        if num_iters % 10000 == 0: print(f"Iterations at {num_iters}. . .")
        x += 1
        row = board[idx_row]
        row_copy = [i for i in row]
        repeat = False
        for idx, cell in enumerate(row):
            if cell == 0:
                possible_row = [i for i in range (1,10) if i not in row]
                possible_col = [i for i in range(1,10) if i not in [board[i][idx] for i in range(0,9)]]
                possible_grid = [i for i in range(1,10) if i not in grid[idx_row // 3][idx // 3]]
                valids = [i for i in possible_row if i in possible_col and i in possible_grid and i != 0]
                if not valids:
                    board[idx_row] = [i for i in row_copy]
                    repeat = True
                    break
                else:
                    cell_answer = random.choice(valids)
                    board[idx_row][idx] = cell_answer
                    grid[idx_row // 3][idx // 3] += [cell_answer]
        if not repeat: idx_row += 1
        if x > max_iterations: board, grid, x, idx_row, num_iters = copy.deepcopy(initial_board), [[[],[],[]],[[],[],[]],[[],[],[]]], 0, 0, num_iters + 1
    print(f"!--BOARD FOUND AFTER {num_iters} iterations and {x} rows--!")
    # for x in board: print(x)
    return board, x
    
def sudokuAnalysis():
    row_tries = 15
    results = []
    initial_start = perf_counter()
    for row_tries in range(10,31,5):
        for i in range(0,100):
            start = perf_counter()
            board = generateInitialGridMatrix()
            board, x = sudokuSolver(board, row_tries)
            end = perf_counter()
            print(f"ITERATION {i+1} FINISHED AT {end - start} SEC. ROWS TO COMPLETE: {x}")
            results.append(f"{i+1},{end - start},{x}")
        print(f"All iterations ended in {perf_counter() - initial_start} sec.")
        with open(f"results{row_tries}_{i+1}.csv","w") as f:
            for x in results: f.write(f"{x}\n")

def threadedSolver(board, n):
    '''Tries to solve sudoku with n threads.'''
    global found
    found = False
    print("INITIAL BOARD")
    for z in board: print(z)
    print(f"Threading with {n} threads")
    def sudokuUp(board):
            global found
            if not found:
                board, x = sudokuSolver(copy.deepcopy(board), 10)
                print(f"!--FOUND SOLUTION--!")
                new_out = ''.join([f"{x}\n" for x in board])
                print(new_out)
                found = True
            else: return
    for x in range(0,n):
        z = threading.Thread(target=sudokuUp, args=(board,), daemon=True)
        z.start()
    while not found: pass

if __name__ == "__main__":
    board = generateInitialGridMatrix()
    for x in board: print(x)
    board, x = sudokuSolver(board, 10)
    for x in board: print(x)
    #board = [[2,0,9,0,6,0,0,3,8],[0,0,4,5,0,8,1,0,0],[6,0,5,0,0,0,4,0,9],[0,5,0,3,4,0,0,2,0],[0,0,0,0,0,1,0,0,0],[4,7,0,0,0,6,8,9,1],[0,0,0,4,2,0,9,1,3],[0,4,2,9,1,0,6,0,0],[0,9,7,0,0,0,2,0,4]]
    #board = [[5,0,0,0,0,0,0,0,1],[0,1,0,0,8,7,0,6,0],[0,0,0,0,0,3,0,0,0],[0,5,0,0,6,1,0,7,0],[0,0,2,0,0,0,9,0,0],[0,0,0,4,0,0,0,0,0],[0,0,0,5,0,0,0,4,0],[9,0,0,0,4,8,7,0,0],[0,8,0,3,0,0,0,0,0]]
    