from enum import Enum
import time
import random
from pandas import *
import pygame

class ListNode:
    def __init__(self, val):
        self.val: SnakeSegment = val
        self.next: ListNode = None
    
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, val):
        node = ListNode(val)
        if self.head is None:
            self.head = node
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            cur.next = node

        self.tail = node

    def as_array(self):
        arr = []
        cur = self.head
        while cur is not None:
            arr.append(cur.val)
            cur = cur.next
        return arr

class SnakeSegment:
    def __init__(self, coords, is_head):
        self.coords = coords
        self.is_head = is_head

    def move(self, direction):
        (x, y) = self.coords
        match direction:
            case Direction.UP:
                self.coords = (x, y-1)
            case Direction.DOWN:
                self.coords = (x, y+1)
            case Direction.RIGHT:
                self.coords = (x+1, y)
            case Direction.LEFT:
                self.coords = (x-1, y)
        


class GameState:
    def __init__(self):
        self.score = 0
        self.goal = (10, 10)
        self.snake = LinkedList()
        self.head_direction = Direction.RIGHT

        snake_head = SnakeSegment((5, 10), True)
        self.snake.add(snake_head)

    def print(self):
        grid = []
        for i in range(32):
            row = []
            for j in range(32):
                row.append(' ')
            grid.append(row)

        snake = self.snake.as_array()
        for i in range(len(snake)):
            (x, y) = snake[i].coords
            grid[x][y] = 'O' if snake[i].is_head else '#'

        (x, y) = self.goal
        grid[x][y] = 'G'

        print(DataFrame(grid))


class SnakeEngine:
    __ignore_conflict_moves = False
    def __init__(self):
        self.restart()

    def restart(self):
        self.state = GameState()
        self.running = True

    def execute_game_tick(self):
        # remember old tail details incase we reach goal
        old_tail = self.state.snake.tail.val
        old_tail_copy = SnakeSegment(old_tail.coords, old_tail.is_head)

        self.move_snake_segments()

        did_snake_collide = self.check_if_collision_occured()
        if did_snake_collide:
            self.running = False

        did_snake_reach_goal = self.check_if_goal_reached()
        if did_snake_reach_goal:
            self.state.score += 100
            self.state.snake.add(old_tail_copy)
            self.place_new_goal()

        #self.state.print()

    def set_head_direction(self, direction):
        if direction is not None:
            if not self.__ignore_conflict_moves or not Direction.is_death_combo(self.state.head_direction, direction):
                self.state.head_direction = direction            

    def move_snake_segments(self):
        cur = self.state.snake.head
        prev_copy = SnakeSegment((cur.val.coords[0], cur.val.coords[1]), True)
        cur.val.move(self.state.head_direction)
        cur = cur.next
        while cur is not None:
            (prev_x, prev_y) = prev_copy.coords
            (x, y) = cur.val.coords
            prev_copy = SnakeSegment((cur.val.coords[0], cur.val.coords[1]), True)
            cur.val.move(self.get_relative_direction(prev_x, prev_y, x, y))
            cur = cur.next

    def get_relative_direction(self, prev_x, prev_y, x, y):
        if prev_x < x:
            return Direction.LEFT
        if prev_x > x:
            return Direction.RIGHT
        if prev_y < y:
            return Direction.UP
        if prev_y > y:
            return Direction.DOWN

    def check_if_collision_occured(self):
        (head_x, head_y) = self.state.snake.head.val.coords
        if (head_x < 0 or head_x >= 32) or (head_y < 0 or head_y >= 32):
            return True
        else:
            cur = self.state.snake.head.next
            while cur is not None:
                snake_segment = cur.val
                if (head_x, head_y) == cur.val.coords:
                    return True
                cur = cur.next

        return False

    def check_if_goal_reached(self):
        return self.state.snake.head.val.coords == self.state.goal

    def place_new_goal(self):
        snake_arr = self.state.snake.as_array()
        while True:
            (x, y) = (random.randrange(32), random.randrange(32))
            for i in range(len(snake_arr)):
                snake_segment_coords = snake_arr[i].coords
                if (x, y) == snake_segment_coords:
                    continue
            break
        self.state.goal = (x, y)


class TileType(Enum):
    SNAKE_HEAD = 1
    SNAKE_BODY = 2
    GOAL = 3
    EMPTY = 0

class Direction():
    UP=1
    DOWN=2
    LEFT=4
    RIGHT=8

    ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
    MOVE_MAP_DEFAULT = {UP: 0, DOWN: 0, LEFT: 0, RIGHT: 0}

    DEATH_INPUT_COMBOS=[UP | DOWN, LEFT | RIGHT]

    def is_death_combo(d1, d2):
        return (d1 | d2) in Direction.DEATH_INPUT_COMBOS
   
######################################################################
# global graphic constants
EMPTY_COLOR = (40, 122, 44)
GOAL_COLOR = (255, 0, 0)
SNAKE_HEAD_COLOR = (40, 122, 255)
SNAKE_BODY_COLOR = (40, 255, 44)

left_px_const = 18
top_px_const = 18

# game constants
tick_rate_seconds = .05

# decision making weightings
towards_goal = 100
not_die = 1000


def get_rect_full(l, t):
    return (l*top_px_const, t*left_px_const, top_px_const, left_px_const)

def get_rect(l, t):
    return (l*top_px_const, t*left_px_const, top_px_const-2, left_px_const-2)

def check_if_event_occured(event):
    return any(e.type == event for e in pygame.event.get())

def check_if_key_pressed(key):
    return pygame.key.get_pressed()[key]

def draw_screen(screen):
    for i in range(32):
        for j in range(32):
            pygame.draw.rect(screen, EMPTY_COLOR, get_rect_full(i, j))

    snake = snake_game_engine.state.snake.as_array()
    for i in range(len(snake)):
        snake_segment = snake[i]
        color = None
        if snake_segment.is_head:
            color = SNAKE_HEAD_COLOR
        else:
            color = SNAKE_BODY_COLOR

        (l, t) = snake_segment.coords
        pygame.draw.rect(screen, color, get_rect(l, t))


    (l, t) = snake_game_engine.state.goal
    pygame.draw.rect(screen, GOAL_COLOR, get_rect_full(l, t))

    # Flip the display
    pygame.display.flip()

def get_direction_from_user_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        return Direction.LEFT
    elif keys[pygame.K_w]:
        return Direction.UP
    elif keys[pygame.K_d]:
        return Direction.RIGHT
    elif keys[pygame.K_s]:
        return Direction.DOWN
    else:
        return None

def always_win(x,y):
    # if x == 0:
    #     return Direction.DOWN
    # if y == 0:
    #     return Direction.LEFT
    if y == 31:
        if x % 2 == 0:
            return Direction.RIGHT
        else:
            return Direction.UP
    if y == 1:
        if x % 2 == 0:
            return Direction.DOWN
        else:
            if x != 31:
                return Direction.RIGHT
            else:
                return Direction.UP
    if y == 0:
        if x != 0:
            return Direction.LEFT
        else:
            return Direction.DOWN

    if x % 2 == 0:
        return Direction.DOWN
    else:
        return Direction.UP

## $$ ##
def get_direction_by_thinking(current_direction, snake, goalx, goaly):
    move_map = Direction.MOVE_MAP_DEFAULT.copy()

    # moving towards goal is good
    (snake_headx, snake_heady) = snake[0].coords
    if snake_headx > goalx:
        move_map[Direction.LEFT] += 100
    if snake_headx < goalx:
        move_map[Direction.RIGHT] += 100
    if snake_heady > goaly:
        move_map[Direction.UP] += 100
    if snake_heady < goaly:
        move_map[Direction.DOWN] += 100

    # if running into wall, bad move
    if snake_headx + 1 >= 32:
        move_map[Direction.RIGHT] = 0
    else:
        move_map[Direction.RIGHT] += 20
    if snake_headx - 1 < 0:
        move_map[Direction.LEFT] = 0
    else:
        move_map[Direction.LEFT] += 20
    if snake_heady + 1 >= 32:
        move_map[Direction.DOWN] = 0
    else:
        move_map[Direction.DOWN] += 20
    if snake_heady - 1 < 0:
        move_map[Direction.UP] = 0
    else:
        move_map[Direction.UP] += 20

    # if running into snake body segment, bad move
    for body_segment in snake:
        if (snake_headx+1, snake_heady) == body_segment.coords:
            move_map[Direction.RIGHT] = 0
        if (snake_headx-1, snake_heady) == body_segment.coords:
            move_map[Direction.LEFT] = 0
        if (snake_headx, snake_heady+1) == body_segment.coords:
            move_map[Direction.DOWN] = 0
        if (snake_headx, snake_heady-1) == body_segment.coords:
            move_map[Direction.UP] = 0

    # not die is good

    # if not any(move_map[direction] > 0 for direction in Direction.ALL_DIRECTIONS):
    #     move_map[random.choice(Direction.ALL_DIRECTIONS)] += 10
    
    # if the death move, bad move
    for potential_dir in Direction.ALL_DIRECTIONS:
        if (potential_dir | current_direction) in Direction.DEATH_INPUT_COMBOS:
            # found the death move
            move_map[potential_dir] = 0
            break

    # print:
    print("{", end="")
    print("UP: " + str(move_map[Direction.UP]), end="")
    print(", DOWN: " + str(move_map[Direction.DOWN]), end="")
    print(", LEFT: " + str(move_map[Direction.LEFT]), end="")
    print(", RIGHT: " + str(move_map[Direction.RIGHT]), end="")
    print("}")
    ########

    # pass to model learner thing

    max_think = 0
    max_dir = None
    for key in move_map.keys():
        if move_map[key] > max_think:
            max_think = move_map[key]
            max_dir = key
    
    return max_dir
## $$ ##
###################################################



# script start entry point below
if __name__ == '__main__':

    # Set up the drawing window
    pygame.init()

    screen = pygame.display.set_mode([576, 576])
    pygame.display.set_caption("SNaiK")
    snake_game_engine = SnakeEngine()

    # Run until the user asks to quit
    user_exited = False
    while not user_exited:

        if check_if_event_occured(pygame.QUIT):
            user_exited = True

        if check_if_key_pressed(pygame.K_SPACE):
            snake_game_engine.restart()
        
        # set next move here
        if snake_game_engine.running:
            snake_game_engine.set_head_direction(get_direction_by_thinking(snake_game_engine.state.head_direction, snake_game_engine.state.snake.as_array(), snake_game_engine.state.goal[0], snake_game_engine.state.goal[1]))
            snake_game_engine.execute_game_tick()
            draw_screen(screen)
        
        time.sleep(tick_rate_seconds)

    # Done! Time to quit.
    pygame.quit()

