import copy


def init_from_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    N = int(lines[0].strip())

    matrix = []

    for line in lines[1:]:
        row = list(map(int, line.split()))
        matrix.append(row)

    return N, matrix


def init_from_terminal():
    N = int(input())
    matrix = []
    for _ in range(N):
        line = input()
        row = list(map(int, line.split()))
        matrix.append(row)

    return N, matrix


# helper function get the column
def get_column(matrix, c):
    return [row[c] for row in matrix]


# helper function to remove zeros from a list
def remove_zeros(list):
    for i in range(len(list) - 1, -1, -1):
        if list[i] == 0:
            del list[i]


def swipe_up(matrix):
    global N
    max = 0
    # split matrix into columns
    for c in range(N):
        column = get_column(matrix, c)

        # get rid of all zeros
        remove_zeros(column)

        # loop through each element in column
        for i in range(len(column) - 1):

            # if number below is same as current number
            if column[i] == column[i + 1]:
                column[i] *= 2
                column[i + 1] = 0

        # remove any zeros have appeared
        remove_zeros(column)

        # replace original matrix with new squished column
        # keep track of maximum value

        for r in range(N):
            if r > len(column) - 1:
                matrix[r][c] = 0
            else:
                max = column[r] if column[r] > max else max
                matrix[r][c] = column[r]

    return max, matrix


def swipe_down(matrix):
    global N
    max = 0
    # split matrix into columns
    for c in range(N):
        column = get_column(matrix, c)

        # get rid of all zeros
        remove_zeros(column)

        # loop through each element in column backwards
        for i in range(len(column) - 1, 0, -1):

            # if number above is same as current number
            if column[i] == column[i - 1]:
                column[i] *= 2
                column[i - 1] = 0

        # remove any zeros have appeared
        remove_zeros(column)

        # replace original matrix with new squished column

        col_idx = len(column) - 1
        for r in range(N - 1, -1, -1):
            if col_idx < 0:
                matrix[r][c] = 0
            else:
                max = column[col_idx] if column[col_idx] > max else max
                matrix[r][c] = column[col_idx]
                col_idx -= 1
    return max, matrix


def swipe_left(matrix):
    global N
    max = 0

    # split matrix into rows
    for r in range(N):
        row = matrix[r][:]

        remove_zeros(row)

        for j in range(len(row) - 1):
            if row[j] == row[j + 1]:
                row[j] *= 2
                row[j + 1] = 0

        remove_zeros(row)

        for c in range(N):
            if c > len(row) - 1:
                matrix[r][c] = 0
            else:
                max = row[c] if row[c] > max else max
                matrix[r][c] = row[c]
    return max, matrix


def swipe_right(matrix):
    global N
    max = 0

    for r in range(N):
        row = matrix[r][:]

        remove_zeros(row)

        for j in range(len(row) - 1, 0, -1):
            if row[j] == row[j - 1]:
                row[j] *= 2
                row[j - 1] = 0

        remove_zeros(row)

        row_idx = len(row) - 1
        for c in range(N - 1, -1, -1):
            if row_idx < 0:
                matrix[r][c] = 0
            else:
                max = row[row_idx] if row[row_idx] > max else max
                matrix[r][c] = row[row_idx]
                row_idx -= 1
    return max, matrix


def swipe(matrix, direction):
    if direction == UP:
        max, return_matrix = swipe_up(matrix)
    elif direction == DOWN:
        max, return_matrix = swipe_down(matrix)
    elif direction == LEFT:
        max, return_matrix = swipe_left(matrix)
    elif direction == RIGHT:
        max, return_matrix = swipe_right(matrix)

    return max, return_matrix


file_init = False
N = 0
original_matrix = []
if file_init:
    N, original_matrix = init_from_file("input.txt")
else:
    N, original_matrix = init_from_terminal()

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

MOVE_COUNT = 0
MAX = 0

EXPLORED_MATRICES = []


# function to check if matrix has already been checked
def check_explored(matrix):
    # loop through each explored space
    for i in range(len(EXPLORED_MATRICES)):
        # check each space if it matches
        if matrix == EXPLORED_MATRICES[i]:
            return True

    return False


# function to add matrix to explored
def add_to_explored(matrix, max_value):
    global EXPLORED_MATRICES
    global MAX

    EXPLORED_MATRICES.append(matrix)
    if max_value > MAX:
        MAX = max_value


# recursively check the movespace
def iterate(matrix, MOVE_COUNT):
    global MAX
    # iterate_up = False
    # iterate_down = False
    # iterate_right = False
    # iterate_left = False

    if MOVE_COUNT != 5:
        # swipe up down left right
        up_max, up_matrix = swipe(copy.deepcopy(matrix), UP)
        down_max, down_matrix = swipe(copy.deepcopy(matrix), DOWN)
        left_max, left_matrix = swipe(copy.deepcopy(matrix), LEFT)
        right_max, right_matrix = swipe(copy.deepcopy(matrix), RIGHT)

        if up_max > MAX:
            MAX = up_max
        if down_max > MAX:
            MAX = down_max
        if left_max > MAX:
            MAX = left_max
        if right_max > MAX:
            MAX = right_max

        MOVE_COUNT += 1

        # only iterate if the matrix has not been seen before
        # if iterate_up:
        iterate(up_matrix, MOVE_COUNT)
        # if iterate_down:
        iterate(down_matrix, MOVE_COUNT)
        # if iterate_left:
        iterate(left_matrix, MOVE_COUNT)
        # if iterate_right:
        iterate(right_matrix, MOVE_COUNT)


iterate(matrix=original_matrix, MOVE_COUNT=MOVE_COUNT)


# print(swipe(copy.deepcopy(original_matrix), UP))
# print(swipe(copy.deepcopy(original_matrix), DOWN))
# print(swipe(copy.deepcopy(original_matrix), LEFT))
# print(swipe(copy.deepcopy(original_matrix), RIGHT))
print(MAX)


# create movespace with original matrix
