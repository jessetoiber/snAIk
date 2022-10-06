from enum import Enum
from pandas import *
import random

class ListNode:
    def __init__(self, val):
        self.val: SnakeSegment = val
        self.next: ListNode = None
    
# snake represented by a linked list as the data structure
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

        grid = list(zip(*grid[::-1]))
        grid = list(zip(*grid[::-1]))
        grid = list(zip(*grid[::-1]))

        print("\n----\n")
        print(DataFrame(grid))

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