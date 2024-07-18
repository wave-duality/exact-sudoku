from PIL import Image
import numpy as np
import random

def sudoku_to_exact_cover(grid):
    rows = []
    rows_to_remove = []
    cols_to_remove = []
    for r in range(9):
        for c in range(9):
            for n in range(9):
                #324 columns total
                #729 rows total, for this specific row:
                #constraint 1 (value): column 9*r + c should be ticked
                #constraint 2 (row): column 81 + 9*r + n should be ticked
                #constraint 3 (column): column 162 + 9*c + n should be ticked
                #constraint 4 (squares): column 243 + 27*(r/3) + 9*(c/3) + n
                row = [0 for i in range(324)]
                row[9*r+c] = 1
                row[81+9*r+n] = 1
                row[162+9*c+n] = 1
                row[243+27*(r//3)+9*(c//3)+n] = 1
                rows.append(row)
            if grid[9*r+c] != '.':
                val = int(grid[9*r+c])-1
                #first, remove the 4 constraints that this satisfies
                cols_to_remove.append(9*r+c) 
                cols_to_remove.append(81+9*r+val)
                cols_to_remove.append(162+9*c+val)
                cols_to_remove.append(243+27*(r//3)+9*(c//3)+val)
    for i in range(len(rows)):
        for j in cols_to_remove:
            if rows[i][j] == 1:
                rows_to_remove.append(i)
    rows = np.array(rows)
    rows = np.delete(rows, rows_to_remove, axis=0)
    rows = np.delete(rows, cols_to_remove, axis=1)
    rows = rows.tolist()
    return rows

def shuffle(m):
    rows = [i for i in range(len(m))]
    cols = [i for i in range(len(m[0]))]
    random.shuffle(rows)
    random.shuffle(cols)
    m = [m[j] for j in rows]
    for k in m:
        k = [k[j] for j in cols]
    return m

def visualize(sudoku, s):
    rows = sudoku_to_exact_cover(sudoku)
    if s:
        rows = shuffle(rows)
    img = Image.new('1', (len(rows[0]), len(rows)))
    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i, j] = rows[j][i]

    img.show()

class DancingLinks:
    def __init__(self, matrix):
        self.header = self.build_linked_matrix(matrix)
        self.solution_count = 0

    class Node:
        def __init__(self):
            self.left = self.right = self.up = self.down = self.column = self

    class ColumnNode(Node):
        def __init__(self, name):
            super().__init__()
            self.name = name
            self.size = 0

    def build_linked_matrix(self, matrix):
        # Build the column headers
        header = self.ColumnNode("header")
        column_nodes = []
        for i in range(len(matrix[0])):
            column_node = self.ColumnNode(str(i))
            column_nodes.append(column_node)
            column_node.left = header.left
            column_node.right = header
            header.left.right = column_node
            header.left = column_node
        
        # Build the linked matrix
        for i in range(len(matrix)):
            prev = None
            for j in range(len(matrix[i])):
                if matrix[i][j] == 1:
                    col_node = column_nodes[j]
                    new_node = self.Node()
                    new_node.column = col_node

                    new_node.up = col_node.up
                    new_node.down = col_node
                    col_node.up.down = new_node
                    col_node.up = new_node

                    if prev is None:
                        prev = new_node
                    else:
                        new_node.left = prev
                        new_node.right = prev.right
                        prev.right.left = new_node
                        prev.right = new_node

                    col_node.size += 1
                    prev = new_node
        
        return header

    def cover(self, col_node):
        col_node.right.left = col_node.left
        col_node.left.right = col_node.right
        node = col_node.down
        while node != col_node:
            right_node = node.right
            while right_node != node:
                right_node.down.up = right_node.up
                right_node.up.down = right_node.down
                right_node.column.size -= 1
                right_node = right_node.right
            node = node.down

    def uncover(self, col_node):
        node = col_node.up
        while node != col_node:
            left_node = node.left
            while left_node != node:
                left_node.column.size += 1
                left_node.down.up = left_node
                left_node.up.down = left_node
                left_node = left_node.left
            node = node.up
        col_node.right.left = col_node
        col_node.left.right = col_node

    def search(self, k=0):
        if self.header.right == self.header:
            self.solution_count += 1
            return
        col_node = self.select_column_node()
        self.cover(col_node)
        row_node = col_node.down
        while row_node != col_node:
            right_node = row_node.right
            while right_node != row_node:
                self.cover(right_node.column)
                right_node = right_node.right
            self.search(k + 1)
            left_node = row_node.left
            while left_node != row_node:
                self.uncover(left_node.column)
                left_node = left_node.left
            row_node = row_node.down
        self.uncover(col_node)

    def select_column_node(self):
        col_node = self.header.right
        min_size = col_node.size
        current = col_node.right
        while current != self.header:
            if current.size < min_size:
                col_node = current
                min_size = current.size
            current = current.right
        return col_node

def count_exact_covers(matrix):
    dlx = DancingLinks(matrix)
    dlx.search()
    return dlx.solution_count

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve_sudoku(board):
    empty = find_empty_location(board)
    if not empty:
        return True
    row, col = empty
    numbers = list(range(1, 10))
    random.shuffle(numbers)
    for num in numbers:
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def generate_sudoku():
    board = [[0] * 9 for _ in range(9)]
    solve_sudoku(board)
    return board

def board_to_string(board):
    return ''.join(str(board[row][col]) for row in range(9) for col in range(9))

# Generate and print a fully solved Sudoku board in 81-character format

k = ".1..2...323......145.1.3267583....1.1.2....3...431..2.341...67....471352725.3.14."
print(count_exact_covers(sudoku_to_exact_cover(k)))
'''
FINDING SUDOKUS WITH EXACTLY K-SOLS
k = "1...........12.....5....1........7.8......645.....9..223189.576.652.1.84..4..6..."
visualize(k, False)
print(count_exact_covers(sudoku_to_exact_cover(k)))

with open('sudokuresults.txt', 'r') as f:
    data = f.read()
    solutions = {}
    data = data.split("\n")
    for i in data:
        l = i.split(" ")
        if len(l[0]) > 0:
            solutions[int(l[0])] = l[1]
unseen = []
for i in range(1,1001):
    if i not in solutions:
        unseen.append(i)
print(unseen)
print(len(solutions))
p = 0.58 #chance of removing every number
for i in range(50000):
    b = board_to_string(generate_sudoku())
    for j in range(len(b)):
        n = random.random()
        if n < p:
            b = b[:j] + '.' + b[j+1:]
    if b.count('.') < 55 and b.count('.') > 40:
        k = count_exact_covers(sudoku_to_exact_cover(b))
        if k not in solutions and k <= 1000:
            solutions[k] = b
            print("Updated: " + str(len(solutions)))
    if i % 1000 == 0:
        print("Done with: " + str(i) + " tests.")

with open('sudokuresults.txt', 'w') as f:
    for i in sorted(solutions.keys()):
        f.write(str(i) + " " + str(solutions[i]) + "\n")
'''

'''
DOING SOME DISTRIBUTION STUFF TESTING
'''
distr_data = [] #collecting data on relationship between removing n clues and number of possible sols
for i in range(41,56):
    distr = {}
    for n in range(20000):
        b = board_to_string(generate_sudoku())
        cells = [_ for _ in range(81)]
        random.shuffle(cells)
        removal = cells[:i]
        for k in removal:
            b = b[:k] + '.' + b[k+1:]
        c = count_exact_covers(sudoku_to_exact_cover(b))
        if c not in distr:
            distr[c] = 1
        else:
            distr[c] += 1
    distr_data.append([i, distr])
    print(str(i), distr)
with open('sudokudistr3.txt', 'w') as f:
    for i in distr_data:
        f.write(str(i[0]) + " ")
        f.write(str(dict(sorted(i[1].items()))))
        f.write("\n")

'''
SIMPLE BACKTRACKING CODE TO FIND ALL SOLUTIONS TO A PUZZLE
'''
def is_valid(board, row, col, num):
    # Check if the number is not in the current row, column and 3x3 sub-grid
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def find_empty_cell_with_mrv(board):
    min_options = 10
    best_cell = None
    for row in range(9):
        for col in range(9):
            if board[row][col] == '.':
                options = [num for num in '123456789' if is_valid(board, row, col, num)]
                if len(options) < min_options:
                    min_options = len(options)
                    best_cell = (row, col)
                    if min_options == 1:
                        return best_cell
    return best_cell

def solve_sudoku(board, solutions):
    empty_cell = find_empty_cell_with_mrv(board)
    if not empty_cell:
        # Join the board into a single 81-char string
        solutions.append(''.join(''.join(row) for row in board))
        return

    row, col = empty_cell
    for num in '123456789':
        if is_valid(board, row, col, num):
            board[row][col] = num
            solve_sudoku(board, solutions)
            board[row][col] = '.'

def find_all_solutions(puzzle_str):
    # Parse the input string into a 2D list
    board = [[puzzle_str[i * 9 + j] for j in range(9)] for i in range(9)]
    solutions = []
    solve_sudoku(board, solutions)
    return solutions

def resolve(sols):
    res = ""
    for i in range(len(sols[0])):
        var = True
        k = sols[0][i]
        for l in sols:
            if l[i] != k:
                var = False
        if var == True:
            res = res + k
        else:
            res = res + '.'
    return res

'''
new = []
with open('sudokuresults.txt', 'r') as f:
    d = f.read().split("\n")[:-1]
    for k in d:
        n = k.split(" ")[0]
        res = resolve(find_all_solutions(k.split(" ")[1]))
        new.append([n, res])
        print(n)

with open('sudokuresultsresolved.txt', 'w') as f:
    for i in new:
        f.write(i[0] + " " + i[1] + "\n")
'''

'''
def normalize(sudoku):
    #make it so that the appearances of numbers go in order
    res = ""
    curr = 1
    m = {}
    for i in sudoku:
        if i != '.':
            if i not in m:
                m[i] = curr
                curr += 1
    for i in sudoku:
        if i == '.':
            res = res + '.'
        else:
            res = res + str(m[i])
    return res

new = []
with open('sudokuresultsresolved.txt', 'r') as f:
    d = f.read().split("\n")[:-1]
    for k in d:
        n = k.split(" ")[0]
        res = normalize(k.split(" ")[1])
        new.append([n, res])

with open('sudokuresultsstandardized.txt', 'w') as f:
    for i in new:
        f.write(i[0] + " " + i[1] + "\n")
'''