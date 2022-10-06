# SNaiK program entry point for multiple threaded games at once  
import threading
from src.start_game import start_game

if __name__ == '__main__':
    for i in range(0,4):
        x = threading.Thread(target=start_game)
        x.start()
