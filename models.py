from enum import Enum
import random

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