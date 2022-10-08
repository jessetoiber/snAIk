from src.game.game_models import *
from src.game.game_next_move_decision_helpers import *
from src.game.game_graphics import *
from pathlib import Path
from datetime import datetime

import time
import sys
class GameEngine:
    __ignore_conflict_moves = False
    def __init__(self):
        self.restart()

        self.gamestate_df_data_output_file = None
        if len(sys.argv) >= 2:
            Path("data").mkdir(exist_ok=True)
            file_name_without_ext = Path(sys.argv[1]).stem
            gamestate_df_data_output_path = 'data/' + file_name_without_ext + datetime.now().strftime('__%m-%d-%y_%I%M%S') + '.txt'
            self.gamestate_df_data_output_file = Path(gamestate_df_data_output_path).open('a')

    def restart(self):
        self.state = GameState()
        self.window = GameGraphicsWindow()
        self.snake_still_alive = True
        self.running = True
    
    def quit(self):
        self.running = False

        if self.gamestate_df_data_output_file is not None: 
            print("Gamestate dataframe data recorded at: " + self.gamestate_df_data_output_file.name)
            self.gamestate_df_data_output_file.close()

    def execute_game_tick(self, tick_speed_seconds):
        # if user closed game window
        if GameGraphicsWindow.check_if_user_quit():
            self.quit()
            return

        if GameGraphicsWindow.check_if_user_restart():
            self.restart()
            return
        
        time.sleep(tick_speed_seconds)

        if not self.snake_still_alive:
            self.window.display_restart_game_text()
            return

        # do the actual moving
        direction = self.__get_next_direction_for_head()

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
            old_tail_copy.is_head = False
            self.state.snake.add(old_tail_copy)
            self.place_new_goal()

        self.window.draw_screen(self.state)

        if self.gamestate_df_data_output_file is not None:
            self.gamestate_df_data_output_file.write(self.state.to_string() + '\n\n')


    def __get_next_direction_for_head(self):
        # here we control how to decide the snake's next move
        #
        # return get_player_manual_move_input()
        #   OR
        # return always_win(self.state.goal[0], self.state.goal[1])
        #   OR
        return get_direction_by_thinking(self.state.head_direction, self.state.snake.as_array(), self.state.goal[0], self.state.goal[1])

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