from pandas import *
from game.game_models import *
from game.game_engine import *
from game.game_graphics import *
from game.game_next_move_decision_helpers import *
import time

# game constants
tick_rate_seconds = .001

def run_snake_game():
    game_engine = GameEngine()
    game_graphics_window = GameGraphicsWindow()

    # Run until the user asks to quit
    while True:
        # if user closed game window
        if GameGraphicsWindow.check_if_user_quit():
            break

        if GameGraphicsWindow.check_if_user_restart():
            game_engine.restart()

        if not game_engine.snake_still_alive:
            game_graphics_window.display_restart_game_text()
        else:
            run_single_game_move(game_engine)
            game_graphics_window.draw_screen(game_engine.state)

        time.sleep(tick_rate_seconds)


# moves the board exactly one move
def run_single_game_move(engine):
    # control how the sname decides next move
    
    # eg1) move_direction = get_player_manual_move_input()
    # eg2) move_direction = always_win(snake_game_engine.state.goal[0], snake_game_engine.state.goal[1])
    move_direction = get_direction_by_thinking(engine.state.head_direction, engine.state.snake.as_array(), engine.state.goal[0], engine.state.goal[1])
    
    engine.execute_game_tick(move_direction)