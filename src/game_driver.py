from pandas import *
import pygame
from models import *
from game_engine import *
import time

## GLOBAL CONSTANTS

# graphic constants
EMPTY_COLOR = (40, 122, 44)
GOAL_COLOR = (255, 0, 0)
SNAKE_HEAD_COLOR = (40, 122, 255)
SNAKE_BODY_COLOR = (40, 255, 44)
RESTART_TXT_COLOR = (255, 255, 255)
SCREEN_WIDTH = SCREEN_HEIGHT = 576
left_px_const = 18
top_px_const = 18
#

# game constants
tick_rate_seconds = .001
#

# decision making weightings
towards_goal = 100
not_die = 1000
#

## END GLOBAL CONSTANTS

def run_snake_game():
    snake_game_engine = SnakeEngine()
    screen = init_game_window()

    # Run until the user asks to quit
    while True:
        # if user closed game window
        if check_if_event_occured(pygame.QUIT):
            break

        # spacebar key to reset the game
        if check_if_key_pressed(pygame.K_SPACE):
            snake_game_engine.restart()

        if not snake_game_engine.snake_still_alive:
            display_restart_game_text(screen)
        else:
            run_single_game_move(snake_game_engine)
            draw_screen(screen, snake_game_engine.state)

        time.sleep(tick_rate_seconds)

    pygame.quit()

def init_game_window():    
    pygame.init()
    pygame.font.init() 
    pygame.display.set_caption("SNaiK: he just wants to be real.")
    return pygame.display.set_mode([SCREEN_HEIGHT, SCREEN_WIDTH])

# moves the board exactly one move
def run_single_game_move(engine):
    # control how the sname decides next move
    
    # eg1) move_direction = get_direction_from_user_input()
    # eg2) move_direction = always_win(snake_game_engine.state.goal[0], snake_game_engine.state.goal[1])
    move_direction = get_direction_by_thinking(engine.state.head_direction, engine.state.snake.as_array(), engine.state.goal[0], engine.state.goal[1])
    
    engine.set_head_direction(move_direction)
    engine.execute_game_tick()


def get_rect_full(l, t):
    return (l*top_px_const, t*left_px_const, top_px_const, left_px_const)

def get_rect(l, t):
    return (l*top_px_const, t*left_px_const, top_px_const-2, left_px_const-2)

def check_if_event_occured(event):
    return any(e.type == event for e in pygame.event.get())

def check_if_key_pressed(key):
    return pygame.key.get_pressed()[key]

def draw_screen(screen, gamestate):
    for i in range(32):
        for j in range(32):
            pygame.draw.rect(screen, EMPTY_COLOR, get_rect_full(i, j))

    snake = gamestate.snake.as_array()
    for i in range(len(snake)):
        snake_segment = snake[i]
        color = None
        if snake_segment.is_head:
            color = SNAKE_HEAD_COLOR
        else:
            color = SNAKE_BODY_COLOR

        (l, t) = snake_segment.coords
        pygame.draw.rect(screen, color, get_rect(l, t))


    (l, t) = gamestate.goal
    pygame.draw.rect(screen, GOAL_COLOR, get_rect_full(l, t))
    pygame.display.flip()

def display_restart_game_text(screen):
    font = pygame.font.SysFont('Courier', 30)
    text_surface = font.render("  Press <spacebar> to restart  ", True, (0, 0, 0)) 
    screen.blit(text_surface, (0, 0))
    pygame.display.flip()


# can be used if you want to play the game via WASD keyboard input
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

# use as the next move function to demo the "always win" cheese
def always_win(x,y):
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



