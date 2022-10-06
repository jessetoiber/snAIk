from game_models import *

class GameEngine:
    __ignore_conflict_moves = False
    def __init__(self):
        self.restart()

    def restart(self):
        self.state = GameState()
        self.snake_still_alive = True

    def execute_game_tick(self, direction):
        if direction is not None:
            if not self.__ignore_conflict_moves or not Direction.is_death_combo(self.state.head_direction, direction):
                self.state.head_direction = direction

        # remember old tail details incase we reach goal
        old_tail = self.state.snake.tail.val
        old_tail_copy = SnakeSegment(old_tail.coords, old_tail.is_head)

        self.move_snake_segments()

        did_snake_collide = self.check_if_collision_occured()
        if did_snake_collide:
            self.snake_still_alive = False

        did_snake_reach_goal = self.check_if_goal_reached()
        if did_snake_reach_goal:
            self.state.score += 100
            self.state.snake.add(old_tail_copy)
            self.place_new_goal()

        #self.state.print()      

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