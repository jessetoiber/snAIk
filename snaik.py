import time
from pandas import *
import pygame
from models import *

   
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

