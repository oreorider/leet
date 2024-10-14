RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3


def read_from_file(filename):
    with open(filename, "r") as file:
        input = file.readlines()
    N = int(input[0].strip())
    K = int(input[1].strip())

    apples = []

    for apple in input[2 : 2 + K]:
        apples.append(list(map(int, apple.split())))

    moves = []
    L = int(input[2 + K].strip())
    for move in input[3 + K : 3 + K + L]:
        move_pair = move.split()
        moves.append([int(move_pair[0]), str(move_pair[1])])

    return N, K, apples, L, moves


def read_from_terminal():
    N = int(input())
    K = int(input())
    apples = []
    for _ in range(K):
        apples.append(list(map(int, input().split())))

    moves = []
    L = int(input())
    for _ in range(L):
        move_pair = input().split()
        moves.append([int(move_pair[0]), str(move_pair[1])])

    return N, K, apples, L, moves


class SnakeNode:
    def __init__(self, next=None, prev=None, x=None, y=None):
        self.next = next
        self.prev = prev
        self.x = x
        self.y = y


class Snake:
    def __init__(self, head: SnakeNode, tail: SnakeNode, direction: int):
        self.head = head
        self.tail = tail
        self.direction = direction

    def rotate(self, new_direction: str):
        # turn left
        if new_direction == "L":
            if self.direction == 3:
                self.direction = 0
            else:
                self.direction += 1

        # turn right
        if new_direction == "D":
            if self.direction == 0:
                self.direction = 3
            else:
                self.direction -= 1

    def move(self):
        # get new head coordinates
        if self.direction == RIGHT:
            new_x = self.head.x + 1
            new_y = self.head.y
        elif self.direction == UP:
            new_x = self.head.x
            new_y = self.head.y - 1
        elif self.direction == LEFT:
            new_x = self.head.x - 1
            new_y = self.head.y
        elif self.direction == DOWN:
            new_x = self.head.x
            new_y = self.head.y + 1

        # create new snakenode that will be the new head
        new_head = SnakeNode(prev=self.head, x=new_x, y=new_y)

        # update head
        self.head.next = new_head
        self.head = new_head

    def delete_tail(self):
        # update tail
        new_tail = self.tail.next
        self.tail.next = None
        self.tail = new_tail

    def check_collision(self):
        segment = self.tail
        # no collision possible if snake is 1 long
        if self.tail == self.head:
            return False

        # loop through snake segments to check collisions
        while segment != self.head:
            # if snake segment is same location as head, collision!
            if [segment.x, segment.y] == [self.head.x, self.head.y]:
                return True
            else:
                segment = segment.next


# returns number of seconds snake moves, and if game if finished or not
def move_snake(
    snake: Snake, move_seconds: int, new_direction: str, apples: list[int, int]
):
    global N
    seconds_moved = 0
    # move snake for move_seconds
    for _ in range(move_seconds):
        snake.move()
        # check if snake runs into wall
        seconds_moved += 1
        if snake.head.x < 1 or snake.head.x > N or snake.head.y < 1 or snake.head.y > N:
            return seconds_moved, True

        # check if snake runs into itself
        elif snake.check_collision() == True:
            return seconds_moved, True

        else:
            # if snake has not run into apple, keep same length
            if [snake.head.y, snake.head.x] not in apples:
                snake.delete_tail()
            else:
                apples.remove([snake.head.y, snake.head.x])

    # turn snake
    snake.rotate(new_direction=new_direction)

    return seconds_moved, False


# main function
apples = []
moves = []

submit = True
# init game state
if submit:
    N, K, apples, L, moves = read_from_terminal()
else:
    N, K, apples, L, moves = read_from_file("input.txt")
total_seconds = 0

# init snake
snake_head = SnakeNode(x=1, y=1)
snake_tail = snake_head
snake = Snake(head=snake_head, tail=snake_tail, direction=RIGHT)
game_over = False

# move snake
for move in moves:
    seconds, game_finished = move_snake(
        snake=snake,
        move_seconds=move[0] - total_seconds,
        new_direction=move[1],
        apples=apples,
    )
    total_seconds += seconds
    if game_finished:
        game_over = True
        break

# move snake in straight line until game ends if game has not finished uet
if not game_over:
    while True:
        seconds, game_finished = move_snake(
            snake=snake, move_seconds=10000, new_direction="L", apples=apples
        )
        total_seconds += seconds
        if game_finished:
            break
print(total_seconds)
