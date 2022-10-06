from src.game.game_models import *
from src.game.game_engine import *
from src.game.game_next_move_decision_helpers import *

# game constants
__tick_rate_seconds = .001

def drive_game():
    game_engine = GameEngine()

    # Run until the user asks to quit
    while game_engine.running:
        game_engine.execute_game_tick(__tick_rate_seconds)


