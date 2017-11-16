from itertools import product
import random
import copy
import timeit
import argparse

def solve_sudoku(size, grid):
    R, C = size
    N = R * C
    X = ([("rc", rc) for rc in product(range(N), range(N))] +
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
         [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
         [("bn", bn) for bn in product(range(N), range(1, N + 1))])
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // R) * R + (c // C) # Box number
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n))]
    X, Y = exact_cover(X, Y)
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n:
                select(X, Y, (i, j, n))
    for solution in solve(X, Y, []):
        for (r, c, n) in solution:
            grid[r][c] = n
        yield grid

def exact_cover(X, Y):
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X, Y

def solve(X, Y, solution):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()


def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols


def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)


def get_random_num(sudoku, index): 
    candidate = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    row = int(index / 9)
    col = index % 9

    grid_x = int(row / 3) * 3
    grid_y = int(col / 3) * 3

    j = 0
    while j < col:
        if sudoku[row * 9 + j] in candidate:
            candidate.remove(sudoku[row * 9 + j])
        j += 1

    i = 0
    while i < row:
        if sudoku[i * 9 + col] in candidate:
            candidate.remove(sudoku[i * 9 + col])
        i += 1

    for _i in range(0, 3):
        for _j in range(0, 3):
            if sudoku[(grid_x + _i) * 9 + grid_y + _j] in candidate:
                candidate.remove(sudoku[(grid_x + _i) * 9 + grid_y + _j])

    if len(candidate) == 0:   
        random_num = -1
    else:
        random_num = random.choice(candidate)

    return random_num


def sudoku_generate_backtracking():
    sudoku = [0] * 81
    i = 0
    while i < 81:
        random_num = get_random_num(sudoku, i)  
        if random_num == -1:  
            sudoku = [0] * 81
            i = 0
        else:
            sudoku[i] = random_num
            i += 1
    return sudoku


def unique_answer(grid):
    generator = solve_sudoku((3, 3), grid)
    count = 0
    try:
        while 1:
            next(generator)
            count += 1
    except StopIteration:
        # print("here")
        pass
    if count > 1:
        return False
    return True


def generate(args):
    max_iter = args.size
    full_sudoku = sudoku_generate_backtracking()
    # print(full_sudoku)
    full_sudoku = [full_sudoku[x:x+9] for x in range(0,81,9)]
    # print(full_sudoku)

    enable_pairs = [(i, j) for i in range(9) for j in range(9)]

    sudoku = full_sudoku
    random_pair = random.choice(enable_pairs)

    i=0
    j=0

    while i < max_iter:

        sudoku_tmp = copy.deepcopy(sudoku)

        sudoku_tmp[random_pair[0]][random_pair[1]] = 0
        flag = unique_answer(sudoku_tmp)

        if flag:
            i += 1
            sudoku[random_pair[0]][random_pair[1]] = 0
            enable_pairs.remove(random_pair)
            random.shuffle(enable_pairs)
            j = 0
        else:
            j += 1
            if j >= len(enable_pairs):
                break
        random_pair = enable_pairs[j]

    # print(sudoku)
    # print(i)

    for i in range(9):
        result = ''
        for j in range(9):
            if sudoku[i][j] == 0:
                result +='.'
            else:
                result += str(sudoku[i][j])
        print(result)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--size', type=int, 
        required=True, help='number of maximum blank in 9*9 sudoku')  
    
    args = parser.parse_args()
    
    start = timeit.default_timer()
    generate(args)
    stop = timeit.default_timer()

    print("runtime = " + str(stop - start))

if __name__ == '__main__':
    main()