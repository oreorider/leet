def read_matrix_from_file(filename):
    with open(filename, 'r') as file:
        # Read all lines from the file
        lines = file.readlines()
    
    # Get the matrix size from the first line
    size = int(lines[0].strip())
    
    # Initialize the matrix
    matrix = []
    
    # Parse the remaining lines to fill the matrix
    for line in lines[1:]:
        row = list(map(int, line.split()))
        matrix.append(row)
    
    return size, matrix

def read_matrix_from_terminal():
    size = input()
    matrix = []
    for _ in range (int(size)):
        line = input()
        row = list(map(int, line.split()))
        matrix.append(row)
        
    return int(size), matrix


filename = 'input.txt'
#N, matrix = read_matrix_from_file(filename)
N, matrix = read_matrix_from_terminal()
        
disperse_matrix = [
    [0, 0, 2, 0, 0],
    [0, 10, 7, 1, 0],
    [5, 'alpha', 0, 0, 0],
    [0, 10, 7, 1, 0],
    [0, 0, 2, 0, 0]
]

center = [int(N/2), int(N/2)]
LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3
current_direction = LEFT
travel_amount = 1
travel_count = 0
direction_list = [LEFT, DOWN, RIGHT, UP]
amount_expelled = 0

# function to update tornado direction and travel amount
def update_direction_and_travel():
    global current_direction
    global travel_count
    global travel_amount
    
    # if tornado moved fully in one direction
    if travel_amount == travel_count:
        # increase travel amount if needed
        if current_direction == DOWN or current_direction == UP:
            travel_amount += 1
        # change direction
        current_direction = direction_list[(current_direction + 1) % 4]
        travel_count = 0

# function to update disperse matrix
def update_dispersion():
    global disperse_matrix
    if current_direction == LEFT:
        disperse_matrix = [
            [0, 0, 2, 0, 0],
            [0, 10, 7, 1, 0],
            [5, 'alpha', 0, 0, 0],
            [0, 10, 7, 1, 0],
            [0, 0, 2, 0, 0]
        ]
    elif current_direction == DOWN:
        disperse_matrix = [
            [0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [2, 7, 0, 7, 2],
            [0, 10, 'alpha', 10, 0],
            [0, 0, 5, 0, 0]
        ]
    elif current_direction == RIGHT:
        disperse_matrix = [
            [0, 0, 2, 0, 0],
            [0, 1, 7, 10, 0],
            [0, 0, 0, 'alpha', 5],
            [0, 1, 7, 10, 0],
            [0, 0, 2 ,0, 0]
        ]
    # UP
    else:
        disperse_matrix = [
            [0, 0, 5, 0, 0],
            [0, 10, 'alpha', 10, 0],
            [2, 7, 0, 7, 2],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0]
        ]
    

# move tornado until center at (0,0)
while center != [0,0]:
    
    # move tornado by 1
    if current_direction == LEFT:
        center[1] -= 1
    elif current_direction == DOWN:
        center[0] += 1 
    elif current_direction == RIGHT:
        center[1] += 1
    else:
        center[0] -= 1
    travel_count += 1
    
    # move sand
    original_amount = matrix[center[0]][center[1]]
    leftover = original_amount
    matrix[center[0]][center[1]] = 0
    
    i_disp = 0
    j_disp = 0
    i_alpha = 0
    j_alpha = 0
    
    # loop through elements in matrix that are going to disperse
    for i in range(center[0] - 2, center[0] + 3):
        for j in range(center[1] - 2, center[1] + 3):            
            
            # if alpha spot do later
            if disperse_matrix[i_disp][j_disp] == 'alpha':
                # remember the location
                i_alpha = i
                j_alpha = j
                j_disp += 1
                continue
            
            # amount of sand to be moved
            amount = int(original_amount * (disperse_matrix[i_disp][j_disp] * 0.01))
            
            # leftover sand
            leftover -= amount  
            
            # if sand out of bounds
            if i < 0 or i >= N or j < 0 or j >= N:
                amount_expelled += amount
            
            # if not out of bounds
            else:
                matrix[i][j] += amount
                
            j_disp += 1
        j_disp = 0
        i_disp += 1
        
    # add leftover
    if i_alpha < 0 or i_alpha >= N or j_alpha < 0 or j_alpha >= N:
        amount_expelled += leftover
    else:
        matrix[i_alpha][j_alpha] += leftover
        
    
    # update travel amoun
    
    # update direction and travel amount
    update_direction_and_travel()
    
    # update dispersion
    update_dispersion()
    
print(amount_expelled)
    