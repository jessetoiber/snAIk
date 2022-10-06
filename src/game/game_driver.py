from src.game.game_engine import *

__tick_rate_seconds = .008

def drive_game():
    game_engine = GameEngine()

    while game_engine.running:
        game_engine.execute_game_tick(__tick_rate_seconds)